from collections import defaultdict
from datetime import datetime
from odoo import models, api

class SaleOrderReport(models.AbstractModel):
    _name = 'report.dvz_purchase_bom.purchase_order_report_template'
    _description = 'Weekly Sales Order Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        sale_orders = self.env['sale.order'].browse(data['sale_order_ids'])

        # Dictionary to store weekly sales data
        weekly_sales = defaultdict(lambda: defaultdict(float))
        unique_weeks = set()
        unique_products = set()

        for order in sale_orders.filtered(lambda o: o.state == 'sale'):  # Filter confirmed orders
            week_number = order.date_order.isocalendar()[1]
            year = order.date_order.year
            unique_weeks.add(week_number)

            for line in order.order_line:
                product = line.product_id.name
                # Only add valid product names (non-False, non-empty strings)
                if product and isinstance(product, str):
                    unique_products.add(product)
                    # weekly_sales[(year, week_number)][product] += line.product_uom_qty

                # Get product name and add to report
                product = line.product_id
                if product and product.name:
                    unique_products.add(product.name)
                    weekly_sales[(year, week_number)][product.name] += line.product_uom_qty

                    # Step 1: Get Manufacturing Orders linked to this sale order and product
                    manufacturing_orders = self.env['mrp.production'].search([
                        ('origin', '=', order.name),
                        ('product_id', '=', product.id)
                    ])

                    for mo in manufacturing_orders:
                        mo_product = mo.product_id.name
                        print(f"Manufactured Product: {mo_product}")

                        # Step 2: Get raw materials from BoM used in the MO
                        for raw_material_line in mo.move_raw_ids:
                            raw_product = raw_material_line.product_id.name
                            raw_qty = raw_material_line.product_uom_qty
                            print(f"  └─ Raw Material: {raw_product} ({raw_qty})")

        sorted_weeks = sorted(unique_weeks)
        sorted_products = sorted(unique_products)

        return {
            'data': data,
            'docs': sale_orders,
            'weekly_sales': weekly_sales,
            'weeks': sorted_weeks,
            'products': sorted_products,
            'year': 2025  # Modify dynamically if needed
        }