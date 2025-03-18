from collections import defaultdict
from odoo import models, api

class CustomerSalesReport(models.AbstractModel):
    _name = 'report.customer_weekly_sales_report.sales_report'
    _description = 'Weekly Customer Sales Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        sale_orders = self.env['sale.order'].browse(data['sale_order_ids'])

        weekly_sales = defaultdict(lambda: defaultdict(float))
        unique_weeks = set()
        unique_customers = set()

        for order in sale_orders:
            week_number = order.date_order.isocalendar()[1]
            unique_weeks.add(week_number)
            customer = order.partner_id.name
            unique_customers.add(customer)

            for line in order.order_line:
                weekly_sales[customer][week_number] += line.product_uom_qty

        sorted_weeks = sorted(unique_weeks)
        sorted_customers = sorted(unique_customers)

        return {
            'data': data,
            'docs': sale_orders,
            'weekly_sales': weekly_sales,
            'weeks': sorted_weeks,
            'customers': sorted_customers,
        }
