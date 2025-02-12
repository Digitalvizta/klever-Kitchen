# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from base64 import encodebytes
from datetime import datetime
from io import BytesIO
from pytz import timezone, utc
from xlwt import Workbook, easyxf
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT


class SaleProductIndentWizard(models.TransientModel):
    _name = 'sh.sale.product.indent.wizard'
    _description = 'Sale Product Indent Wizard'

    sh_start_date = fields.Datetime(
        'Start Date', required=True, default=fields.Datetime.now)
    sh_end_date = fields.Datetime(
        'End Date', required=True, default=fields.Datetime.now)
    sh_partner_ids = fields.Many2many(
        'res.partner', string='Customers')
    sh_status = fields.Selection([('all', 'All'), ('draft', 'Draft'), ('sent', 'Quotation Sent'), (
        'sale', 'Sales Order'), ('done', 'Locked')], default='all', string='Status')
    sh_category_ids = fields.Many2many(
        'product.category', string='Categories')
    company_ids = fields.Many2many(
        'res.company', default=lambda self: self.env.companies, string="Companies")

    @api.constrains('sh_start_date', 'sh_end_date')
    def _check_dates(self):
        if self.filtered(lambda c: c.sh_end_date and c.sh_start_date > c.sh_end_date):
            raise ValidationError(_('start date must be less than end date.'))

    def print_report(self):
        datas = self.read()[0]
        return self.env.ref('sh_sale_reports.sh_sale_product_indent_action').report_action([], data=datas)

    def display_report(self):
        datas = self.read()[0]
        report = self.env['report.sh_sale_reports.sh_sale_product_indent_doc']
        data_values = report._get_report_values(
            docids=None, data=datas).get('order_dic')
        self.env['sh.product.sales.indent'].search([]).unlink()
        if data_values:
            for key in data_values:
                for category_data in data_values[key]:
                    for key2 in category_data:
                        for data in category_data[key2]:
                            self.env['sh.product.sales.indent'].create({
                                'name': data['product_id'],
                                'quantity': data['qty'],
                                'sh_partner_id': data['partner_id'],
                                'sh_category_id': data['category_id'],
                            })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Product Sales Indent',
            'view_mode': 'list',
            'res_model': 'sh.product.sales.indent',
            'context': "{'create': False,'search_default_group_customer': 1}"
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
            'Sales Product Indent', bold_center)
        worksheet.write_merge(
            0, 1, 0, 1, 'Sales Product Indent', heading_format)
        center = easyxf('align: horiz center;')
        bold_center_total = easyxf('align: horiz center;font:bold True')
        user_tz = self.env.user.tz or utc
        local = timezone(user_tz)
        start_date = datetime.strftime(utc.localize(datetime.strptime(str(
            self.sh_start_date), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local), DEFAULT_SERVER_DATETIME_FORMAT)
        end_date = datetime.strftime(utc.localize(datetime.strptime(str(
            self.sh_end_date), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local), DEFAULT_SERVER_DATETIME_FORMAT)
        worksheet.write_merge(2, 2, 0, 1, start_date + " to " + end_date, bold)
        worksheet.col(0).width = int(40 * 260)
        worksheet.col(1).width = int(40 * 260)

        # Get Data
        datas = self.read()[0]
        report = self.env['report.sh_sale_reports.sh_sale_product_indent_doc']
        order_dic = report._get_report_values(
            docids=None, data=datas).get('order_dic')

        row = 4
        if order_dic:
            for key in order_dic:
                worksheet.write(row, 0, key, bold)
                worksheet.write_merge(row, row, 0, 1, key, bold)
                row = row + 2
                for category_data in order_dic[key]:
                    for key_2 in category_data:
                        total = 0.0
                        worksheet.write_merge(row, row, 0, 1, key_2, bold)
                        row = row + 1
                        worksheet.write(row, 0, "Product", bold_center_total)
                        worksheet.write(row, 1, "Quantity", bold_center_total)
                        row = row + 1
                        for record in category_data[key_2]:
                            total = total + record.get('qty')
                            worksheet.write(row, 0, record.get('name'), center)
                            worksheet.write(row, 1, "{:.2f}".format(
                                record.get('qty')), center)
                            row = row + 1
                        worksheet.write(row, 0, "Total", bold_center_total)
                        worksheet.write(row, 1, "{:.2f}".format(
                            total), bold_center_total)
                        row = row + 2

        filename = ('Sales Product Indent' + '.xls')
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

        attachment = ir_attachment.search(
            [('name', '=', filename),
             ('type', '=', 'binary'),
             ('res_model', '=', 'ir.ui.view')], limit=1)

        if attachment:
            attachment.write(attachment_vals)
        else:
            attachment = ir_attachment.create(attachment_vals)

        url = '/web/content/' + str(attachment.id) + '?download=true'
        return {'type': 'ir.actions.act_url', 'url': url,
                'target': 'new'}
