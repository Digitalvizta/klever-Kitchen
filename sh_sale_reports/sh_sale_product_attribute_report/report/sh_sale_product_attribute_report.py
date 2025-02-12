# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, api,_
from odoo.exceptions import UserError

class SaleProductReport(models.AbstractModel):
    _name = 'report.sh_sale_reports.sh_sale_product_report'
    _description = 'Sale Product report abstract model'

    @api.model
    def _get_report_values(self, docids, data=None):
        '''Get selected data from wizard '''

        data = dict(data or {})
        sh_partner_ids = data['sh_partner_ids']
        sh_from_date = data['sh_from_date']
        sh_to_date = data['sh_to_date']
        sh_category_ids = data['sh_category_ids']
        sh_select_product_cat = data['sh_select_product_cat']
        sh_vertical_attribute_id = data['sh_vertical_attribute_id']
        sh_horizontal_attribute_id = data['sh_horizontal_attribute_id']
        sh_product_ids = data['sh_product_ids']
        sh_sale_order_stage = data['sh_sale_order_stage']
        sh_company_id = self.env['res.company'].sudo().search(
            [('id', '=', data.get('sh_company_id')[0])])
        vals = []

        # Selected Attibute getting from wizard
        if sh_vertical_attribute_id and sh_horizontal_attribute_id:
            if sh_partner_ids:
                partner_ids = self.env['res.partner'].sudo().search(
                    [('id', 'in', sh_partner_ids), '|', ('company_id', '=', sh_company_id.id), ('company_id', '=', False)])
            else:
                partner_ids = self.env['res.partner'].sudo().search([
                    ('id', '>', 0), '|', ('company_id', '=', sh_company_id.id), ('company_id', '=', False)])
            if sh_sale_order_stage == 'all':
                domain = [('date_order', '>=', sh_from_date), ('date_order',
                                                               '<=', sh_to_date), ('partner_id', 'in', partner_ids.ids)]
            elif sh_sale_order_stage == 'draft':
                domain = [('date_order', '>=', sh_from_date), ('date_order', '<=', sh_to_date), (
                    'state', 'in', ['draft', 'sent']), ('partner_id', 'in', partner_ids.ids)]
            elif sh_sale_order_stage == 'sale':
                domain = [('date_order', '>=', sh_from_date), ('date_order', '<=', sh_to_date),
                          ('state', '=', 'sale'), ('partner_id', 'in', partner_ids.ids)]
            elif sh_sale_order_stage == 'done':
                domain = [('date_order', '>=', sh_from_date), ('date_order', '<=', sh_to_date),
                          ('state', '=', 'done'), ('partner_id', 'in', partner_ids.ids)]
            domain.append(('company_id', '=', sh_company_id.id))
            sh_sale_order = self.env['sale.order'].sudo().search(domain)
            horizontal_attr_list = []
            vertical_attr_list = []
            sh_horizontal_attribute_id = self.env['product.attribute'].sudo().search(
                [('id', '=', sh_horizontal_attribute_id[0])])
            sh_vertical_attribute_id = self.env['product.attribute'].sudo().search(
                [('id', '=', sh_vertical_attribute_id[0])])
            horizontal_attr_ids_list = sh_horizontal_attribute_id.value_ids.ids
            vertical_attr_ids_list = sh_vertical_attribute_id.value_ids.ids
            for i in range(0, len(sh_horizontal_attribute_id.value_ids.ids)):
                horizontal_attr_list.append(
                    sh_horizontal_attribute_id.value_ids[i].name)
            for j in range(0, len(sh_vertical_attribute_id.value_ids.ids)):
                vertical_attr_list.append(
                    sh_vertical_attribute_id.value_ids[j].name)
            partner_list = []
            category_list = []
            product_list = []
            count=0
            # Get record Product wise.

            if sh_select_product_cat == 'product' and sh_product_ids:
                product_ids = self.env['product.product'].sudo().search(
                    [('id', 'in', sh_product_ids), '|', ('company_id', '=', sh_company_id.id), ('company_id', '=', False)])
            else:
                product_ids = self.env['product.product'].sudo().search([
                    ('id', '>', 0), '|', ('company_id', '=', sh_company_id.id), ('company_id', '=', False)])
            if sh_select_product_cat == 'category' and sh_category_ids:
                category_ids = self.env['product.category'].sudo().search(
                    [('id', 'in', sh_category_ids)])
            else:
                category_ids = self.env['product.category'].sudo().search([
                    ('id', '>', 0)])

            # Select Product according to attribute

            product_attribute_dict = {}
            if sh_select_product_cat == 'product' and product_ids:
                order_lines = self.env['sale.order.line'].sudo().search(
                    [('product_id', 'in', product_ids.ids), ('order_id', 'in', sh_sale_order.ids)])
            if sh_select_product_cat == 'category' and category_ids:
                order_lines = self.env['sale.order.line'].sudo().search(
                    [('product_id.categ_id', 'in', category_ids.ids), ('order_id', 'in', sh_sale_order.ids)])
            for order in order_lines:
                x_qty = 0
                y_qty = 0
                x = -1
                y = -1
                attribute_list = []
                for x in range(0, len(vertical_attr_ids_list)):
                    attribute_list.append([])
                    for y in range(0, len(horizontal_attr_ids_list)):
                        attribute_list[x].append(0)
                if order.order_id.partner_id.name in partner_list:
                    pass
                else:
                    partner_list.append(order.order_id.partner_id.name)
                    product_attribute_dict[order.order_id.partner_id.name] = {}

                # Get record category wise.

                if order.product_id:
                    if sh_select_product_cat == 'category':
                        if order.product_id.categ_id.display_name in product_attribute_dict[order.order_id.partner_id.name].keys():
                            pass
                        else:
                            category_list.append(
                                order.product_id.categ_id.display_name)
                            product_attribute_dict[order.order_id.partner_id.name][order.product_id.categ_id.display_name] = {
                            }
                    if sh_select_product_cat == 'category':
                        if order.product_id.name in list(product_attribute_dict[order.order_id.partner_id.name][order.product_id.categ_id.display_name].keys()):
                            pass
                        else:
                            product_attribute_dict[order.order_id.partner_id.name][
                                order.product_id.categ_id.display_name][order.product_id.name] = attribute_list
                    else:
                        if order.product_id.name in product_attribute_dict[order.order_id.partner_id.name].keys():
                            pass
                        else:
                            product_attribute_dict[order.order_id.partner_id.name][order.product_id.name] = attribute_list
                    if order.product_id.name in product_list:
                        pass
                    else:
                        product_list.append(order.product_id.name)

                    if sh_select_product_cat == 'category':
                        for att in order.product_id.product_template_attribute_value_ids:
                            if att.attribute_id.id == sh_horizontal_attribute_id.id:
                                x = horizontal_attr_list.index(att.name)
                                x_qty = order.product_uom_qty
                            if att.attribute_id.id == sh_vertical_attribute_id.id:
                                y = vertical_attr_list.index(att.name)
                                y_qty = order.product_uom_qty
                            if x_qty > 0 and y_qty > 0 and x > -1 and y > -1:
                                count+=1
                                product_attribute_dict[order.order_id.partner_id.name][
                                    order.product_id.categ_id.display_name][order.product_id.name][y][x] += y_qty
                    else:
                        for att in order.product_id.product_template_attribute_value_ids:
                            if att.attribute_id.id == sh_horizontal_attribute_id.id:
                                x = horizontal_attr_list.index(att.name)
                                x_qty = order.product_uom_qty
                            if att.attribute_id.id == sh_vertical_attribute_id.id:
                                y = vertical_attr_list.index(att.name)
                                y_qty = order.product_uom_qty
                            if x_qty > 0 and y_qty > 0 and x > -1 and y > -1:
                                count+=1
                                product_attribute_dict[order.order_id.partner_id.name][order.product_id.name][y][x] += y_qty

        # Prepare vals for print report.
        if product_attribute_dict and count>0:
            vals.append({
                'sh_from_date': sh_from_date,
                'sh_to_date': sh_to_date,
                'sh_select_product_cat': sh_select_product_cat,
                'horizontal_attr_list': horizontal_attr_list,
                'vertical_attr_list': vertical_attr_list
            })

            return{
                'vals': vals,
                'sale_product': product_attribute_dict,
            }
        else:
            raise UserError(_('There is no data in between these dates.....'))
