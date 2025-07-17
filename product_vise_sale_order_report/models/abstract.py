from collections import defaultdict
from datetime import datetime, date
from odoo import models, api

class SaleOrderReport(models.AbstractModel):
    _name = 'report.product_vise_sale_order_report.batch_output_temp'
    _description = 'Weekly Sales Order Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        sale_orders = self.env['sale.order'].browse(data['sale_order_ids'])

        weekly_outputs = defaultdict(lambda: defaultdict(float))
        unique_weeks = set()
        products = set()

        for order in sale_orders.filtered(lambda o: o.state == 'sale'):
            week_number = order.fulfill_order_date.isocalendar()[1]
            year = order.fulfill_order_date.year
            unique_weeks.add(week_number)

            # Find parent MRP production orders where origin matches sale order name
            parent_mrp_orders = self.env['mrp.production'].search([
                ('origin', '=', order.name),
                ('state', '!=', 'cancel')
            ])

            # Find all MRP orders linked to the sale order's procurement group
            procurement_group = order.procurement_group_id
            all_mrps = parent_mrp_orders
            if procurement_group:
                related_mrps = self.env['mrp.production'].search([
                    ('procurement_group_id', '=', procurement_group.id),
                    ('state', '!=', 'cancel')
                ])
                all_mrps |= related_mrps  # Include related MRPs (potential child orders)

            for mrp_order in all_mrps:
                product_name = mrp_order.product_id.name
                products.add(product_name)
                batch_output = mrp_order.batch_output or 0.0  # Assume batch_output is a Float field

                # Sum batch_output for the product in the corresponding week
                weekly_outputs[(year, week_number)][product_name] += float(batch_output)

        sorted_weeks = sorted(unique_weeks)
        sorted_products = sorted(products)

        return {
            'data': data,
            'docs': sale_orders,
            'weekly_boms': weekly_outputs,  # Kept key name for compatibility
            'weeks': sorted_weeks,
            'products': sorted_products,
            'year': date.today().year,
        }