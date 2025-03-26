from collections import defaultdict
from datetime import datetime, date
from odoo import models, api
from odoo.tools.safe_eval import json


class SaleOrderReport(models.AbstractModel):
    _name = 'report.product_vise_sale_order_report.batch_output_temp'
    _description = 'Weekly Sales Order Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        sale_orders = self.env['sale.order'].browse(data['sale_order_ids'])

        weekly_boms = defaultdict(lambda: defaultdict(float))
        unique_weeks = set()
        bom_products = set()

        for order in sale_orders.filtered(lambda o: o.state == 'sale'):
            week_number = order.date_order.isocalendar()[1]
            year = order.date_order.year
            unique_weeks.add(week_number)

            for line in order.order_line:
                # Find BOMs for this product
                matching_boms = self.env['boms.boms'].search([
                    ('product_id', '=', line.product_id.product_tmpl_id.id)
                ])

                for bom in matching_boms:
                    for bom_line in bom.bom_line_ids:
                        component_product = bom_line.product_id.name
                        bom_products.add(component_product)

                        # Add BOM quantities
                        try:
                            week_data = json.loads(bom_line.week_data or "{}")
                            bom_qty = week_data.get(str(week_number), bom_line.qty)
                            weekly_boms[(year, week_number)][component_product] += bom_qty * line.product_uom_qty
                        except (json.JSONDecodeError, ValueError):
                            weekly_boms[(year, week_number)][component_product] += bom_line.qty * line.product_uom_qty

        sorted_weeks = sorted(unique_weeks)
        sorted_products = sorted(bom_products)

        return {
            'data': data,
            'docs': sale_orders,
            'weekly_boms': weekly_boms,
            'weeks': sorted_weeks,
            'products': sorted_products,
            'year': date.today().year,
        }