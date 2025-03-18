from datetime import date, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CustomerSalesReportWizard(models.TransientModel):
    _name = 'customer.sales.report.wizard'
    _description = 'Customer Weekly Sales Report Wizard'

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
        next_month = today.replace(day=28) + timedelta(days=4)  # Move to next month
        last_day = next_month - timedelta(days=next_month.day)  # Get last day of the month
        return last_day

    def action_print_customer_report(self):
        if self.start_date > self.end_date:
            raise UserError(_("Start Date cannot be greater than End Date."))

        sale_orders = self.env['sale.order'].search([
            ('date_order', '>=', self.start_date),
            ('date_order', '<=', self.end_date),
            ('state', '=', 'sale'),
        ])
        print(sale_orders)

        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'sale_order_ids': sale_orders.ids
        }

        return self.env.ref('customer_weekly_sales_report.action_customer_sales_report').report_action(self, data=data)
