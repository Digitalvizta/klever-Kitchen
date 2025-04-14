from collections import defaultdict
from datetime import date, timedelta
import json
from odoo import api, fields, models, _


class ProductBoms(models.Model):
    _name = 'boms.boms'
    _description = 'BOMs Model'

    name = fields.Char(string='Name')
    number = fields.Char("Reference",
                         default=lambda self: _('New'),
                         copy=False, readonly=True, tracking=True)
    product_id = fields.Many2one('product.template', string='Main Product')

    bom_line_ids = fields.One2many('product.vise.boms', 'boms_id')

    @api.model_create_multi
    def create(self, vals_list):
        """ Generate a sequence for the BOMs model """
        for vals in vals_list:
            if vals.get('number', _('New')) == _('New'):
                vals['number'] = self.env['ir.sequence'].next_by_code('boms.boms') or _('New')
        return super(ProductBoms, self).create(vals_list)


class ProductViseBoms(models.Model):
    _name = 'product.vise.boms'
    _description = 'Product Vise BOMs'

    boms_id = fields.Many2one('boms.boms')
    product_id = fields.Many2one('product.template', 'Product')
    qty = fields.Float(string='Batch Output')

    week_data = fields.Text(string="Week Data")  # Store weekly quantity data as JSON

    def get_weekly_quantity(self, week):
        """ Returns the quantity for a given week """
        week_data = json.loads(self.week_data or "{}")  # Convert stored data to dictionary
        return week_data.get(str(week), 0)  # Return quantity for the requested week


class BOMReport(models.AbstractModel):
    _name = 'report.product_vise_sale_order_report.boms_boms_temp'
    _description = 'Weekly Sales Order Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        today = date.today()
        start_date = today.replace(day=1)  # First day of the current month
        next_month = today.replace(day=28) + timedelta(days=4)  # Move to next month
        end_date = next_month - timedelta(days=next_month.day)  # Last day of the current month

        # Get sale orders for the current month
        sale_orders = self.env['sale.order'].search([
            ('state', '=', 'sale'),
            ('date_order', '>=', start_date),
            ('date_order', '<=', end_date),
        ])

        weekly_sales = defaultdict(lambda: defaultdict(float))
        weekly_boms = defaultdict(lambda: defaultdict(float))
        unique_weeks = set()
        unique_products = set()

        for order in sale_orders:
            week_number = order.date_order.isocalendar()[1]
            year = order.date_order.year
            unique_weeks.add(week_number)

            for line in order.order_line:
                sale_product = line.product_id

                # Find BOMs where the main product matches the sale order line product
                matching_boms = self.env['boms.boms'].search([
                    ('product_id', '=', sale_product.product_tmpl_id.id)
                ])

                for matching_bom in matching_boms:
                    # Fetch all products inside the matching BOM
                    bom_products = self.env['product.vise.boms'].search([
                        ('boms_id', '=', matching_bom.id)
                    ])

                    for bom_line in bom_products:
                        product = bom_line.product_id
                        unique_products.add(product.name)

                        # Add sale order quantity
                        weekly_sales[(year, week_number)][product.name] += line.product_uom_qty

                        # Fetch BOM quantity data
                        week_data = json.loads(bom_line.week_data or "{}")
                        weekly_boms[(year, week_number)][product.name] += week_data.get(str(week_number), bom_line.qty)

        sorted_weeks = sorted(unique_weeks)
        sorted_products = sorted(unique_products)

        return {
            'data': data,
            'docs': sale_orders,
            'weekly_sales': weekly_sales,
            'weekly_boms': weekly_boms,
            'weeks': sorted_weeks,
            'products': sorted_products,
            'year': today.year,
            'start_date': start_date,
            'end_date': end_date,
        }