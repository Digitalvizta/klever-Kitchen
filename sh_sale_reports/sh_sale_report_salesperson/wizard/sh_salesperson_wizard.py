# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from base64 import encodebytes
from io import BytesIO
from datetime import datetime
from pytz import timezone, utc
from xlwt import Workbook, easyxf
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class SalespersonWizard(models.TransientModel):
    _name = "sh.sale.report.salesperson.wizard"
    _description = "sh sale report salesperson wizard model"

    @api.model
    def default_company_ids(self):
        if is_allowed_companies := self.env.context.get(
            'allowed_company_ids', False
        ):
            return is_allowed_companies
        return False
    
    name = fields.Char(
        string='Name', 
        required=False)

    date_start = fields.Datetime(
        string="Start Date", required=True, default=fields.Datetime.now)
    date_end = fields.Datetime(
        string="End Date", required=True, default=fields.Datetime.now)
    user_ids = fields.Many2many(
        comodel_name="res.users",
        relation="rel_sh_sale_report_salesperson_user_ids",
        string="Salesperson")

    state = fields.Selection([
        ('all', 'All'),
        ('done', 'Done'),
    ], string='Status', default='all', required=True)

    company_ids = fields.Many2many(
        'res.company', string='Companies', default=default_company_ids)

    @api.model
    def default_get(self, fields):
        rec = super(SalespersonWizard, self).default_get(fields)
        search_users = self.env["res.users"].sudo().search(
            [('company_id', 'in', self.env.context.get('allowed_company_ids', False))])
        if self.env.user.has_group('sales_team.group_sale_salesman_all_leads'):
            rec.update({
                "user_ids": [(6, 0, search_users.ids)],
            })
        else:
            rec.update({
                "user_ids": [(6, 0, search_users.ids)],
            })
        return rec

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        if self.filtered(lambda c: c.date_end and c.date_start > c.date_end):
            raise ValidationError(_('start date must be less than end date.'))

    def print_report(self):
        datas = self.read()[0]
        return self.env.ref('sh_sale_reports.sh_sale_report_salesperson_report').report_action([], data=datas)

    def display_report(self):
        datas = self.read()[0]
        report = self.env['report.sh_sale_reports.sh_salesperson_report_doc']
        data_values = report._get_report_values(
            docids=None, data=datas).get('user_order_dic')

        self.env['sh.sale.report.salesperson'].search([]).unlink()
        if data_values:
            for user in data_values:
                for order in data_values[user]:
                    self.env['sh.sale.report.salesperson'].create({
                        'sh_user_id': order['user_id'],
                        'sh_partner_id': order['customer_id'],
                        'name': order['order_number'],
                        'date_order': order['order_date'],
                        'total': order['total'],
                        'paid_amount': order['paid_amount'],
                        'due_amount': order['due_amount']
                    })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Report By Salesperson',
            'view_mode': 'tree',
            'res_model': 'sh.sale.report.salesperson',
            'context': "{'create': False,'search_default_group_salesperson': 1}"
        }

    def print_xls_report(self):
        workbook = Workbook(encoding='utf-8')
        heading_format = easyxf(
            'font:height 300,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
        bold = easyxf(
            'font:bold True,height 215;pattern: pattern solid, fore_colour gray25;align: horiz center')
        bold_center = easyxf(
            'font:height 240,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center;')
        worksheet = workbook.add_sheet(
            'Sale Report by Sales Person', bold_center)
        worksheet.write_merge(
            0, 1, 0, 5, 'Sale Report by Sales Person', heading_format)
        left = easyxf('align: horiz center;font:bold True')

        user_tz = self.env.user.tz or utc
        local = timezone(user_tz)
        start_date = datetime.strftime(utc.localize(datetime.strptime(str(
            self.date_start), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local), DEFAULT_SERVER_DATETIME_FORMAT)
        end_date = datetime.strftime(utc.localize(datetime.strptime(str(
            self.date_end), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local), DEFAULT_SERVER_DATETIME_FORMAT)
        worksheet.write_merge(2, 2, 0, 5, f"{start_date} to {end_date}", bold)
        worksheet.col(0).width = int(30 * 260)
        worksheet.col(1).width = int(30 * 260)
        worksheet.col(2).width = int(18 * 260)
        worksheet.col(3).width = int(18 * 260)
        worksheet.col(4).width = int(18 * 260)
        worksheet.col(5).width = int(18 * 260)
        row = 4

        # Get Data
        datas = self.read()[0]
        report = self.env['report.sh_sale_reports.sh_salesperson_report_doc']
        if data_values_user_order_dic := report._get_report_values(
            docids=None, data=datas
        ).get('user_order_dic'):
            for user in data_values_user_order_dic.keys():
                worksheet.write_merge(
                    row, row, 0, 5, f"Sales Person: {user}", bold_center)
                row = row + 2
                worksheet.write(row, 0, "Order Number", bold)
                worksheet.write(row, 1, "Order Date", bold)
                worksheet.write(row, 2, "Customer", bold)
                worksheet.write(row, 3, "Total", bold)
                worksheet.write(row, 4, "Amount Invoiced", bold)
                worksheet.write(row, 5, "Amount Due", bold)

                row = row + 2
                sum_of_amount_total = 0.0
                total_invoice_amount = 0.0
                total_due_amount = 0.0
                for order in data_values_user_order_dic[user]:
                    worksheet.write(row, 0, order.get('order_number'))
                    worksheet.write(row, 1, str(order.get('order_date')))
                    worksheet.write(row, 2, order.get('customer'))
                    worksheet.write(
                        row, 3, "{:.2f}".format(order.get('total')))
                    worksheet.write(row, 4, "{:.2f}".format(
                        order.get('paid_amount')))
                    worksheet.write(row, 5, "{:.2f}".format(
                        order.get('due_amount')))
                    sum_of_amount_total = sum_of_amount_total + \
                        order.get('total')
                    total_invoice_amount = total_invoice_amount + \
                        order.get('paid_amount')
                    total_due_amount = total_due_amount+order.get('due_amount')
                    row = row + 1
                worksheet.write(row, 2, "Total", left)
                worksheet.write(row, 3, "{:.2f}".format(sum_of_amount_total))
                worksheet.write(row, 4, "{:.2f}".format(total_invoice_amount))
                worksheet.write(row, 5, "{:.2f}".format(total_due_amount))
                row = row + 2

        filename = ('Sales Report By Salesperson' + '.xls')
        fp = BytesIO()
        workbook.save(fp)
        data = encodebytes(fp.getvalue())
        ir_attachment = self.env['ir.attachment']
        attachment_vals = {
            'name': filename,
            'res_model': 'ir.ui.view',
            'type': 'binary',
            'datas': data,
            'public': True,
        }
        fp.close()

        attachment = ir_attachment.search([('name', '=', filename),
                                           ('type', '=', 'binary'), ('res_model', '=', 'ir.ui.view')], limit=1)
        if attachment:
            attachment.write(attachment_vals)
        else:
            attachment = ir_attachment.create(attachment_vals)

        url = f'/web/content/{str(attachment.id)}?download=true'
        return {'type': 'ir.actions.act_url', 'url': url,
                'target': 'new'}
