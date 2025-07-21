from odoo import models, fields, api
from datetime import datetime

# class MrpProduction(models.Model):
#     _inherit = 'mrp.production'
#
#     production_date = fields.Datetime(string='Production Date')
#
#     @api.model
#     def create(self, vals):
#         # Create the MRP record first
#         production = super(MrpProduction, self).create(vals)
#
#         origin = production.origin  # Now safely get from record itself
#         if origin:
#             # Check if any other MRP has the same origin and a production_date
#             existing_mrp = self.search([
#                 ('origin', '=', origin),
#                 ('id', '!=', production.id),
#                 ('production_date', '!=', False)
#             ], limit=1)
#
#             if existing_mrp:
#                 # Use production_date from the existing one
#                 production_date = existing_mrp.production_date
#             else:
#                 # No existing MRP has the date, try getting it from Sale Order
#                 sale_order = self.env['sale.order'].search([('name', '=', origin)], limit=1)
#                 production_date = sale_order.date_order if sale_order else fields.Datetime.now()
#
#             # Update this production record
#             production.production_date = production_date
#
#             # Update all other related MRP records with same origin
#             related_mrps = self.search([('origin', '=', origin)])
#             related_mrps.write({'production_date': production_date})
#
#         return production
from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    production_date = fields.Datetime(string='Production Date')

    def _get_root_origin_and_date(self, origin):
        """Trace back origin chain until a sale order is found or existing production date is available."""
        visited = set()
        current_origin = origin

        while current_origin and current_origin not in visited:
            visited.add(current_origin)

            # Check if origin is a Sale Order
            sale_order = self.env['sale.order'].search([('name', '=', current_origin)], limit=1)
            if sale_order:
                return current_origin, sale_order.date_order

            # Check if origin points to another MRP
            parent_mrp = self.search([('name', '=', current_origin)], limit=1)
            if parent_mrp:
                if parent_mrp.production_date:
                    return current_origin, parent_mrp.production_date
                current_origin = parent_mrp.origin  # Go up one level
            else:
                break

        return None, fields.Datetime.now()

    @api.model
    def create(self, vals):
        production = super().create(vals)
        origin = production.origin

        if origin:
            root_origin, production_date = self._get_root_origin_and_date(origin)

            # Set production_date for this and all MOs sharing that origin chain
            related_mrps = self.search([('origin', '=', origin)])
            (related_mrps | production).write({'production_date': production_date})

        return production



class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    main_bom = fields.Boolean(string="Main BOM")
