# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from datetime import timedelta
from pytz import timezone
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CustomerSalesAnalysis(models.AbstractModel):
    _name = 'report.sh_sale_reports.sh_cus_sale_analysis_doc'
    _description = 'Customer Sales Analysis Report Abstract Model'

    @api.model
    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        sale_order_obj = self.env["sale.order"]
        order_dic_by_orders = {}
        order_dic_by_products = {}
        if data['sh_start_date']:
            date_start = fields.Datetime.from_string(data['sh_start_date'])
        else:
            # start by default today 00:00:00
            user_tz = timezone(self.env.context.get(
                'tz') or self.env.user.tz or 'UTC')
            today = user_tz.localize(fields.Datetime.from_string(
                fields.Date.context_today(self)))
            date_start = today.astimezone(timezone('UTC'))

        if data['sh_end_date']:
            date_stop = fields.Datetime.from_string(data['sh_end_date'])
            # avoid a date_stop smaller than date_start
            if date_stop < date_start:
                date_stop = date_start + timedelta(days=1, seconds=-1)
        else:
            # stop by default today 23:59:59
            date_stop = date_start + timedelta(days=1, seconds=-1)

        if data.get('sh_partner_ids', False):
            partners = self.env['res.partner'].sudo().browse(
                data.get('sh_partner_ids', False))
        else:
            partners = self.env['res.partner'].sudo().search([])

        if partners:
            for partner_id in partners:
                order_list = []
                domain = [
                    ("date_order", ">=", fields.Datetime.to_string(date_start)),
                    ("date_order", "<=", fields.Datetime.to_string(date_stop)),
                    ("partner_id", "=", partner_id.id),
                ]
                if data.get('sh_status') == 'all':
                    domain.append(('state', 'not in', ['cancel']))
                elif data.get('sh_status') == 'draft':
                    domain.append(('state', 'in', ['draft']))
                elif data.get('sh_status') == 'sent':
                    domain.append(('state', 'in', ['sent']))
                elif data.get('sh_status') == 'sale':
                    domain.append(('state', 'in', ['sale']))
                    domain.append(('locked', '=', False))
                elif data.get('sh_status') == 'done':
                    domain.append(('locked', '=', True))
                if data.get('company_ids', False):
                    domain.append(
                        ('company_id', 'in', data.get('company_ids', False)))
                search_orders = sale_order_obj.sudo().search(domain)
                if search_orders:
                    for order in search_orders:
                        if data.get('report_by') == 'order':
                            order_dic = {
                                'order_number': order.name,
                                'order_date': order.date_order,
                                'salesperson': order.user_id.name,
                                'salespersion_id': order.user_id.id,
                                'partner_id': order.partner_id.id,
                                'sale_amount': order.amount_total,
                                'sale_currency_id': order.currency_id.id,
                                'sale_currency_symbol': order.currency_id.symbol,  # For Excel Report
                            }
                            paid_amount = 0.0
                            if order.invoice_ids:
                                for invoice in order.invoice_ids:
                                    if invoice.move_type == 'out_invoice':
                                        paid_amount += invoice.amount_total - invoice.amount_residual
                                    elif invoice.move_type == 'out_refund':
                                        paid_amount += - \
                                            (invoice.amount_total -
                                             invoice.amount_residual)
                            order_dic.update({
                                'paid_amount': paid_amount,
                                'balance_amount': order.amount_total - paid_amount
                            })
                            order_list.append(order_dic)
                        elif data.get('report_by') == 'product' and order.order_line:
                            lines = False
                            if data.get('sh_product_ids'):
                                lines = order.order_line.sudo().filtered(
                                    lambda x: x.product_id.id in data.get('sh_product_ids'))
                            else:
                                products = self.env['product.product'].sudo().search(
                                    [])
                                lines = order.order_line.sudo().filtered(
                                    lambda x: x.product_id.id in products.ids)
                            if lines:
                                for line in lines:
                                    order_dic = {
                                        'order_number': line.order_id.name,
                                        'order_date': line.order_id.date_order,
                                        'partner_id': order.partner_id.id,
                                        'product_name': line.product_id.display_name,
                                        'product_id': line.product_id.id,
                                        'price': line.price_unit,
                                        'qty': line.product_uom_qty,
                                        'discount': line.discount,
                                        'tax': line.price_tax,
                                        'subtotal': line.price_subtotal,
                                        'sale_currency_id': order.currency_id.id,
                                        'sale_currency_symbol': order.currency_id.symbol,  # For Excel Report
                                    }
                                    order_list.append(order_dic)
                search_partner = self.env['res.partner'].sudo().search([
                    ('id', '=', partner_id.id)
                ], limit=1)
                if search_partner and order_list:
                    if data.get('report_by') == 'order':
                        order_dic_by_orders.update(
                            {search_partner.display_name: order_list})
                    elif data.get('report_by') == 'product':
                        order_dic_by_products.update(
                            {search_partner.display_name: order_list})

        data.update({
            'date_start': data['sh_start_date'],
            'date_end': data['sh_end_date'],
            'report_by': data.get('report_by'),
        })

        if data.get('report_by') == 'order':
            if order_dic_by_orders:
                data.update({
                    'order_dic_by_orders': order_dic_by_orders,
                })
                return data
            else:
                raise UserError(
                    _('There is no Data Found between these dates...'))
        elif data.get('report_by') == 'product':
            if order_dic_by_products:
                data.update({
                    'order_dic_by_products': order_dic_by_products,
                })
                return data
            else:
                raise UserError(
                    _('There is no Data Found between these dates...'))

        return data
