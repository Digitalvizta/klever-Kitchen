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
            week_number = order.schedule_delivery_date.isocalendar()[1]
            year = order.schedule_delivery_date.year
            unique_weeks.add(week_number)

            # Find parent MRP production orders where origin matches sale order name
            parent_mrp_orders = self.env['mrp.production'].search([
                ('origin', '=', order.name),
                ('state', '!=', 'cancel')
            ])

            for mrp in parent_mrp_orders:
                # Include parent and child MRP orders
                # Search child MRPs where origin matches parent MRP's name
                child_mrps_by_origin = self.env['mrp.production'].search([
                    ('origin', '=', mrp.name),
                    ('state', '!=', 'cancel')
                ])
                # Combine with children from _get_children method
                all_mrps = mrp | child_mrps_by_origin | mrp._get_children().filtered(lambda p: p.state != 'cancel')

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