from odoo import models, fields, api
from datetime import datetime


class WeeklySalesReportWizard(models.TransientModel):
    _name = 'weekly.sales.report.wizard'
    _description = 'Weekly Sales Report Wizard'

    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)

    def action_generate_report(self):
        # Get sales orders within the selected date range
        sale_orders = self.env['sale.order'].search([

        ], limit=3)

        # Create a dictionary to store the total sales for each product
        product_sales = {}

        for order in sale_orders:
            for line in order.order_line:
                product = line.product_id
                if product not in product_sales:
                    product_sales[product] = 0
                product_sales[product] += line.product_uom_qty

        # Prepare the report data
        report_data = []
        for product, total_sales in product_sales.items():
            report_data.append({
                'product': product.name,
                'total_sales': total_sales,
            })

        # Pass data to the report using report_action and generate it
        return self.env.ref('dev_weekly_sale.report_weekly_sales').report_action(self,
                                                                                     data={'report_data': report_data})