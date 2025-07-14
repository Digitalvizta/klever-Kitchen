from collections import defaultdict
from odoo import models, api

class CustomerSalesReport(models.AbstractModel):
    _name = 'report.customer_weekly_sales_report.sales_report'
    _description = 'Weekly Customer Sales Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        sale_orders = self.env['sale.order'].browse(data['sale_order_ids'])

        # Nested dictionary structure: {customer: {product: {week: quantity}}}
        weekly_sales = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        unique_weeks = set()
        unique_customers = set()
        customer_products = defaultdict(set)  # To store products per customer
        product_counts = {}  # Store product count per customer

        for order in sale_orders:
            # week_number = order.date_order.isocalendar()[1]
            week_number = order.fulfill_order_date.isocalendar()[1]
            unique_weeks.add(week_number)
            customer = order.partner_id.name
            unique_customers.add(customer)

            for line in order.order_line:
                product = line.product_id.name
                customer_products[customer].add(product)  # Track products per customer
                weekly_sales[customer][product][week_number] += line.product_uom_qty

        # Ensure all customers have an entry in customer_products, even if empty
        for customer in unique_customers:
            customer_products.setdefault(customer, set())  # Ensure key exists
            product_counts[customer] = len(customer_products[customer])  # Precompute row span

        sorted_weeks = sorted(unique_weeks)
        sorted_customers = sorted(unique_customers)

        return {
            'data': data,
            'docs': sale_orders,
            'weekly_sales': weekly_sales,
            'weeks': sorted_weeks,
            'customers': sorted_customers,
            'customer_products': customer_products,
            'product_counts': product_counts,  # Include in returned values
        }
