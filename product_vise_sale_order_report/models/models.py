from datetime import date, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class BatchOutput(models.TransientModel):
    _name = 'batch.output'
    _description = 'Batch Output'

    sale_order_id = fields.Many2one('sale.order', string="Sale Order")
    start_date = fields.Date(
        string="Start Date",
        required=True,
        default=lambda self: self._get_start_date()
    )
    end_date = fields.Date(
        string="End Date",
        required=True,
        default=lambda self: self._get_end_date()
    )

    @staticmethod
    def _get_start_date():
        """Returns the first day of the current month"""
        today = date.today()
        return today.replace(day=1)

    @staticmethod
    def _get_end_date():
        """Returns the last day of the current month"""
        today = date.today()
        next_month = today.replace(day=28) + timedelta(days=4)
        return next_month - timedelta(days=next_month.day)

    def action_batch_print_report(self):
        if not self.start_date or not self.end_date:
            raise UserError(_("Please select both Start Date and End Date."))

        if self.start_date > self.end_date:
            raise UserError(_("Start Date cannot be greater than End Date."))

        sale_orders = self.env['sale.order'].search([
            ('date_order', '>=', self.start_date),
            ('date_order', '<=', self.end_date),
        ])

        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'sale_order_ids': sale_orders.ids
        }

        return self.env.ref('product_vise_sale_order_report.batch_output_action').report_action(self, data=data)