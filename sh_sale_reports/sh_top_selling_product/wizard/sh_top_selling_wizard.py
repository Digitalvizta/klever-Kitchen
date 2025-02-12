# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from base64 import encodebytes
from datetime import datetime
from io import BytesIO
from pytz import utc, timezone
from xlwt import Workbook, easyxf
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class TopSellingWizard(models.TransientModel):
    _name = "sh.tsp.top.selling.product.wizard"
    _description = 'Top selling product Transient model to just filter products'

    @api.model
    def default_company_ids(self):
        is_allowed_companies = self.env.context.get(
            'allowed_company_ids', False)
        if is_allowed_companies:
            return is_allowed_companies
        return False

    type = fields.Selection([
        ('basic', 'Basic'),
        ('compare', 'Compare'),
    ], string="Report Type", default="basic")

    date_from = fields.Datetime(
        string='From Date', required=True, default=fields.Datetime.now)
    date_to = fields.Datetime(string='To Date', required=True,
                              default=fields.Datetime.now)
    date_compare_from = fields.Datetime(
        string='Compare From Date', default=fields.Datetime.now)
    date_compare_to = fields.Datetime(
        string='Compare To Date', default=fields.Datetime.now)
    no_of_top_item = fields.Integer(
        string='No of Items', required=True, default=10)
    product_uom_qty = fields.Float(string="Total Qty. Sold")
    team_id = fields.Many2one("crm.team", string="Sales Channel")
    company_ids = fields.Many2many(
        'res.company', string="Companies", default=default_company_ids)

    @api.constrains('date_from', 'date_to')
    def _check_from_to_dates(self):
        if self.filtered(lambda c: c.date_to and c.date_from > c.date_to):
            raise ValidationError(_('from date must be less than to date.'))

    @api.constrains('date_compare_from', 'date_compare_to')
    def _check_compare_from_to_dates(self):
        if self.filtered(lambda c: c.date_compare_to and c.date_compare_from and c.date_compare_from > c.date_compare_to):
            raise ValidationError(
                _('compare from date must be less than compare to date.'))

    @api.constrains('no_of_top_item')
    def _check_no_of_top_item(self):
        if self.filtered(lambda c: c.no_of_top_item <= 0):
            raise ValidationError(
                _('No of items must be positive. or not zero'))

    def print_top_selling_product_report(self):
        self.ensure_one()
        # we read self because we use from date and start date in our core bi logic.(in abstract model)
        data = self.read()[0]
        return self.env.ref('sh_sale_reports.sh_top_selling_product_report_action').report_action([], data=data)

    def display_report(self):
        datas = self.read()[0]
        report = self.env['report.sh_sale_reports.sh_top_selling_product_doc']
        data_values = report._get_report_values(
            docids=None, data=datas)
        data_values_products = data_values.get('products')
        data_values_product_qty = data_values.get('products_qty')
        if self.type == "basic":
            self.env['sh.tsp.top.selling.product'].search([]).unlink()
            length = len(data_values_products)
            for product in range(length):
                self.env['sh.tsp.top.selling.product'].create({
                    'name': data_values_products[product].id,
                    'qty': data_values_product_qty[product]
                })
            return {
                'type': 'ir.actions.act_window',
                'name': 'Top Selling Products',
                'view_mode': 'tree',
                'res_model': 'sh.tsp.top.selling.product',
                'context': "{'create': False,'search_default_group_product': 1}"
            }

    def print_top_selling_product_xls_report(self):
        workbook = Workbook()
        heading_format = easyxf(
            'font:height 300,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
        bold = easyxf(
            'font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left')
        bold_center = easyxf(
            'font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
        left = easyxf('align: horiz left')
        row = 1

        worksheet = workbook.add_sheet(
            'Top Selling Products', cell_overwrite_ok=True)
        if self.type == 'basic':
            worksheet.write_merge(
                0, 1, 0, 2, 'Top Selling Products', heading_format)
        if self.type == 'compare':
            worksheet.write_merge(
                0, 1, 0, 6, 'Top Selling Products', heading_format)

        # Get Data
        datas = self.read()[0]
        report = self.env['report.sh_sale_reports.sh_top_selling_product_doc']
        data_values = report._get_report_values(
            docids=None, data=datas)
        data_values_final_product_list = data_values.get('products')
        data_values_final_product_qty_list = data_values.get('products_qty')
        data_values_final_compare_product_list = data_values.get(
            'compare_products')
        data_values_final_compare_product_qty_list = data_values.get(
            'compare_products_qty')
        data_values_new_products = data_values.get('new_products')
        data_values_lost_products = data_values.get('lost_products')

        user_tz = self.env.user.tz or utc
        local = timezone(user_tz)
        basic_start_date = datetime.strftime(utc.localize(datetime.strptime(str(
            self.date_from), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local), DEFAULT_SERVER_DATETIME_FORMAT)
        basic_end_date = datetime.strftime(utc.localize(datetime.strptime(str(
            self.date_to), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local), DEFAULT_SERVER_DATETIME_FORMAT)
        compare_start_date = datetime.strftime(utc.localize(datetime.strptime(str(
            self.date_compare_from), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local), DEFAULT_SERVER_DATETIME_FORMAT)
        compare_end_date = datetime.strftime(utc.localize(datetime.strptime(str(
            self.date_compare_to), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local), DEFAULT_SERVER_DATETIME_FORMAT)

        worksheet.write(3, 0, 'Date From: ', bold)
        worksheet.write(3, 1, basic_start_date)
        worksheet.write(4, 0, 'Date To: ', bold)
        worksheet.write(4, 1, basic_end_date)

        worksheet.col(0).width = int(25 * 260)
        worksheet.col(1).width = int(25 * 260)
        worksheet.col(2).width = int(14 * 260)

        worksheet.write(6, 0, "#", bold)
        worksheet.write(6, 1, "Product", bold)
        worksheet.write(6, 2, "Qty Sold", bold)
        no = 0
        row = 8

        for index, product in enumerate(data_values_final_product_list):
            no = no + 1
            worksheet.write(row, 0, no, left)
            worksheet.write(row, 1, product.name, left)
            worksheet.write(
                row, 2, data_values_final_product_qty_list[index], left)
            row = row+1

        if self.type == 'compare':
            worksheet.write(3, 4, 'Compare From Date: ', bold)
            worksheet.write(3, 5, compare_start_date)
            worksheet.write(4, 4, 'Compare To Date: ', bold)
            worksheet.write(4, 5,  compare_end_date)

            worksheet.col(4).width = int(25 * 260)
            worksheet.col(5).width = int(25 * 260)
            worksheet.col(6).width = int(14 * 260)
            worksheet.write(6, 4, "#", bold)
            worksheet.write(6, 5, "Compare Product", bold)
            worksheet.write(6, 6, "Qty Sold", bold)

            row = 8
            for index, compare_product in enumerate(data_values_final_compare_product_list):
                worksheet.write(row, 4, index+1, left)
                worksheet.write(
                    row, 5, compare_product.name, left)
                worksheet.write(
                    row, 6, data_values_final_compare_product_qty_list[index], left)
                row = row+1

            row = row+2
            worksheet.write_merge(row, row, 0, 2, 'New Products', bold_center)
            worksheet.write_merge(row, row, 4, 6, 'Lost Products', bold_center)
            row = row+1
            starting_row = row
            if data_values_new_products:
                for lost in data_values_new_products:
                    worksheet.write_merge(
                        starting_row, starting_row, 0, 2, lost.name, left)
                    starting_row = starting_row+1

            if data_values_lost_products:
                for new in data_values_lost_products:
                    worksheet.write_merge(row, row, 4, 6, new.name, left)
                    row = row+1

        filename = ('Top Selling Products' + '.xls')
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
                                           ('type', '=', 'binary'),
                                           ('res_model', '=', 'ir.ui.view')], limit=1)
        if attachment:
            attachment.write(attachment_vals)
        else:
            attachment = ir_attachment.create(attachment_vals)

        url = '/web/content/' + str(attachment.id) + '?download=true'
        return {'type': 'ir.actions.act_url', 'url': url,
                'target': 'new'}
