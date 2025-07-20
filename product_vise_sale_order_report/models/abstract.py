from collections import defaultdict
from datetime import datetime, date
from odoo import models, api

from odoo.fields import Date as OdooDate


class SaleOrderReport(models.AbstractModel):
    _name = 'report.product_vise_sale_order_report.batch_output_temp'
    _description = 'Weekly Sales Order Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        parent_mrps = self.env['mrp.production'].browse(data['mrp_order'])

        data_d = data
        # data = data['data']
        # date_from = data_d['start_date']
        # date_from = data.get('start_date')
        # date_to = data_d.get('end_date')

        # if isinstance(date_from, str):
        #     date_from = OdooDate.from_string(date_from)
        # if isinstance(date_to, str):
        #     date_to = OdooDate.from_string(date_to)

        weekly_outputs = defaultdict(lambda: defaultdict(float))
        unique_weeks = set()
        products = set()

        # Fetch all parent MRP productions in the given date range
        # parent_mrps = self.env['mrp.production'].search([
        #     ('production_date', '>=', date_from),
        #     ('production_date', '<=', date_to),
        #     ('state', '!=', 'cancel'),
        # ])

        for mrp in parent_mrps:
            # Skip if BoM doesn't have main_bom checked
            if not mrp.bom_id or not mrp.bom_id.main_bom:
                continue

            # Get children by origin and by _get_children(), exclude cancelled
            child_mrps_by_origin = self.env['mrp.production'].search([
                ('origin', '=', mrp.name),
                ('state', '!=', 'cancel'),
            ])
            all_mrps = mrp | child_mrps_by_origin | mrp._get_children().filtered(lambda p: p.state != 'cancel')

            for mrp_order in all_mrps:
                if not mrp_order.bom_id or not mrp_order.bom_id.main_bom:
                    continue

                prod_date = mrp_order.production_date
                # if not prod_date or prod_date < date_from or prod_date > date_to:
                #     continue

                week_number = prod_date.isocalendar()[1]
                year = prod_date.year
                unique_weeks.add(week_number)

                product_name = mrp_order.product_id.name
                products.add(product_name)
                batch_output = mrp_order.batch_output or 0.0

                weekly_outputs[(year, week_number)][product_name] += float(batch_output)

        sorted_weeks = sorted(unique_weeks)
        sorted_products = sorted(products)

        return {
            'data': data,
            'weekly_boms': weekly_outputs,
            'weeks': sorted_weeks,
            'products': sorted_products,
            'year': date.today().year,
        }
