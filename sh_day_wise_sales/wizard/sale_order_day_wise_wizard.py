# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from base64 import encodebytes
from io import BytesIO
from datetime import datetime, timedelta
from pytz import utc, timezone
from xlwt import Workbook, easyxf
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import ValidationError, UserError


class SaleOrderReport(models.Model):
    _name = 'sale.order.report'
    _description = 'Sale Order Report'

    @api.model
    def default_company_ids(self):
        is_allowed_companies = self.env.context.get(
            'allowed_company_ids', False)
        if is_allowed_companies:
            return is_allowed_companies
        return False

    start_date = fields.Datetime(
        required=True, readonly=False, default=fields.Datetime.now)
    end_date = fields.Datetime(
        required=True, default=fields.Datetime.now, readonly=False)
    company_ids = fields.Many2many(
        'res.company', string='Companies', default=default_company_ids)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        if self.filtered(lambda c: c.end_date and c.start_date > c.end_date):
            raise ValidationError(_('start date must be less than end date.'))

    def get_product(self):
        if self.start_date:
            date_start = fields.Datetime.from_string(self.start_date)
        else:
            # start by default today 00:00:00
            user_tz = timezone(self.env.context.get(
                'tz') or self.env.user.tz or 'UTC')
            today = user_tz.localize(fields.Datetime.from_string(
                fields.Date.context_today(self)))
            date_start = today.astimezone(timezone('UTC'))

        if self.end_date:
            date_stop = fields.Datetime.from_string(self.end_date)
            # avoid a date_stop smaller than date_start
            if date_stop < date_start:
                date_stop = date_start + timedelta(days=1, seconds=-1)
        else:
            # stop by default today 23:59:59
            date_stop = date_start + timedelta(days=1, seconds=-1)
        if self.start_date and self.end_date:
            if len(self.company_ids.ids) >= 1:
                self._cr.execute('''select pt.name as product_name,
                                        so.date_order as order_date,
                                        pr.id as product_id,
                                        sum(sl.product_uom_qty) as sold_cnt
                                        from sale_order as so 
                                        left join sale_order_line as sl on so.id = sl.order_id
                                        left join product_product as pr on pr.id = sl.product_id
                                        left join product_template as pt on  pr.product_tmpl_id = pt.id
                                        where date_order >= %s and date_order <= %s and so.state in ('sale','done') and so.company_id in %s
                                        group by pt.name,so.date_order,pr.id''', (fields.Datetime.to_string(date_start), fields.Datetime.to_string(date_stop), tuple(self.company_ids.ids)))
                product_detail = self._cr.dictfetchall()
            else:
                self._cr.execute('''select pt.name as product_name,
                                        so.date_order as order_date,
                                        pr.id as product_id,
                                        sum(sl.product_uom_qty) as sold_cnt
                                        from sale_order as so 
                                        left join sale_order_line as sl on so.id = sl.order_id
                                        left join product_product as pr on pr.id = sl.product_id
                                        left join product_template as pt on  pr.product_tmpl_id = pt.id
                                        where date_order >= %s and date_order <= %s and so.state in ('sale','done')
                                        group by pt.name,so.date_order,pr.id''', (fields.Datetime.to_string(date_start), fields.Datetime.to_string(date_stop)))
                product_detail = self._cr.dictfetchall()
            data_list = []
            final_list = []
            if len(product_detail) > 0:
                data_list = self.generate_day_wise_dict(product_detail)
            if data_list:
                for data in data_list:
                    if data not in final_list:
                        final_list.append(data)

            if final_list:
                return final_list
            else:
                raise UserError(_(
                    'There is no Data Found between these dates...'))

    def generate_report_data(self):
        products = self.get_product()
        if products:
            return self.env.ref('sh_sale_reports.action_report_sale_order_day_wise_report').report_action(self)

    def display_report_data(self):
        data_values = self.get_product()
        self.env['sh.sales.day.wise.report'].search([]).unlink()
        if data_values:
            for record in data_values:
                monday = record.get('monday')
                tuesday = record.get('tuesday')
                wednesday = record.get('wednesday')
                thursday = record.get('thursday')
                friday = record.get('friday')
                saturday = record.get('saturday')
                sunday = record.get('sunday')

                total_value = monday+tuesday+wednesday+thursday+friday+saturday+sunday
                self.env['sh.sales.day.wise.report'].create({
                    'name': record['product_id'],
                    'monday': record['monday'],
                    'tuesday': record['tuesday'],
                    'wednesday': record['wednesday'],
                    'thursday': record['thursday'],
                    'friday': record['friday'],
                    'saturday': record['saturday'],
                    'sunday': record['sunday'],
                    'total': total_value,
                })
            return {
                'type': 'ir.actions.act_window',
                'name': 'Days Wise Product Sales',
                'view_mode': 'list',
                'res_model': 'sh.sales.day.wise.report',
                'context': "{'create': False,'search_default_group_product': 1}"
            }

    def print_sale_order_day_wise(self):
        final_list = self.get_product()
        workbook = Workbook()
        heading_format = easyxf(
            'font:height 300,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
        bold = easyxf(
            'font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left')
        center = easyxf('font:bold True;align: horiz center')
        right = easyxf('font:bold True;align: horiz right')
        worksheet = workbook.add_sheet(
            'Days Wise Product Sales', cell_overwrite_ok=True)
        worksheet.write_merge(
            0, 1, 0, 8, 'Days Wise Product Sales', heading_format)
        user_tz = self.env.user.tz or utc
        local = timezone(user_tz)
        start_date = datetime.strftime(utc.localize(datetime.strptime(str(
            self.start_date), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local), DEFAULT_SERVER_DATETIME_FORMAT)
        end_date = datetime.strftime(utc.localize(datetime.strptime(str(
            self.end_date), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local), DEFAULT_SERVER_DATETIME_FORMAT)
        worksheet.write_merge(3, 3, 0, 0, "Start Date : ", bold)
        worksheet.write_merge(3, 3, 1, 1, start_date)
        worksheet.write_merge(3, 3, 6, 7, "End Date : ", bold)
        worksheet.write_merge(3, 3, 8, 8, end_date)

        worksheet.col(0).width = int(25*260)
        worksheet.col(1).width = int(14*260)
        worksheet.col(2).width = int(14*260)
        worksheet.col(3).width = int(14*260)
        worksheet.col(4).width = int(14*260)
        worksheet.col(5).width = int(14*260)
        worksheet.col(6).width = int(14*260)
        worksheet.col(7).width = int(14*260)
        worksheet.col(8).width = int(14*260)

        worksheet.write(5, 0, "Product Name", bold)
        worksheet.write(5, 1, "Monday", bold)
        worksheet.write(5, 2, "Tuesday", bold)
        worksheet.write(5, 3, "Wednesday", bold)
        worksheet.write(5, 4, "Thursday", bold)
        worksheet.write(5, 5, "Friday", bold)
        worksheet.write(5, 6, "Saturday", bold)
        worksheet.write(5, 7, "Sunday", bold)
        worksheet.write(5, 8, "Total", bold)
        monday_total = 0
        tuesday_total = 0
        wednesday_total = 0
        thursday_total = 0
        friday_total = 0
        saturday_total = 0
        sunday_total = 0
        row = 6

        if final_list:
            for product in final_list:
                reg = 0
                worksheet.write(row, 0, product['product']['en_US'])
                worksheet.write(row, 1, product['monday'])
                worksheet.write(row, 2, product['tuesday'])
                worksheet.write(row, 3, product['wednesday'])
                worksheet.write(row, 4, product['thursday'])
                worksheet.write(row, 5, product['friday'])
                worksheet.write(row, 6, product['saturday'])
                worksheet.write(row, 7, product['sunday'])
                if product['monday']:
                    monday_total += product['monday']
                    reg += product['monday']
                if product['tuesday']:
                    tuesday_total += product['tuesday']
                    reg += product['tuesday']
                if product['wednesday']:
                    wednesday_total += product['wednesday']
                    reg += product['wednesday']
                if product['thursday']:
                    thursday_total += product['thursday']
                    reg += product['thursday']
                if product['friday']:
                    friday_total += product['friday']
                    reg += product['friday']
                if product['saturday']:
                    saturday_total += product['saturday']
                    reg += product['saturday']
                if product['sunday']:
                    sunday_total += product['sunday']
                    reg += product['sunday']
                worksheet.write(row, 8, reg, right)
                row += 1

        row += 1
        worksheet.write(row, 0, "Total", center)
        worksheet.write(row, 1, monday_total, right)
        worksheet.write(row, 2, tuesday_total, right)
        worksheet.write(row, 3, wednesday_total, right)
        worksheet.write(row, 4, thursday_total, right)
        worksheet.write(row, 5, friday_total, right)
        worksheet.write(row, 6, saturday_total, right)
        worksheet.write(row, 7, sunday_total, right)
        worksheet.write(row, 8, monday_total+tuesday_total+wednesday_total +
                        thursday_total+friday_total+saturday_total+sunday_total, right)

        filename = ('Days Wise Product Sales' + '.xls')
        fp = BytesIO()
        workbook.save(fp)
        data = encodebytes(fp.getvalue())
        ir_ttachment = self.env['ir.attachment']
        attachment_vals = {
            'name': filename,
            'res_model': 'ir.ui.view',
            'type': 'binary',
            'datas': data,
            'public': True,
        }
        fp.close()

        attachment = ir_ttachment.search([('name', '=', filename),
                                          ('type', '=', 'binary'),
                                          ('res_model', '=', 'ir.ui.view')], limit=1)
        if attachment:
            attachment.write(attachment_vals)
        else:
            attachment = ir_ttachment.create(attachment_vals)

        url = '/web/content/' + str(attachment.id) + '?download=true'
        return {'type': 'ir.actions.act_url', 'url': url,
                'target': 'new'}

    def generate_day_wise_dict(self, product_detail):
        data_dict = {}

        for product_dic in product_detail:
            product_id = product_dic['product_id']
            product_name = product_dic['product_name']
            order_date = product_dic['order_date']
            day_of_week = order_date.weekday()
            sold_cnt = int(product_dic['sold_cnt'])

            if (product_id, day_of_week) not in data_dict:
                data_dict[(product_id, day_of_week)] = {
                    'product_id': product_id,
                    'product': product_name,
                    'monday': 0,
                    'tuesday': 0,
                    'wednesday': 0,
                    'thursday': 0,
                    'friday': 0,
                    'saturday': 0,
                    'sunday': 0
                }

            # Update the sales count for the corresponding day
            data_dict[(product_id, day_of_week)
                      ][self.weekday_to_key(day_of_week)] += sold_cnt

        # Convert the dictionary values to a list
        data_list = list(data_dict.values())

        return data_list

    def weekday_to_key(self, day_index):
        weekdays = ['monday', 'tuesday', 'wednesday',
                    'thursday', 'friday', 'saturday', 'sunday']
        return weekdays[day_index]
