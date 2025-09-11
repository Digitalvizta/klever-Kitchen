from odoo import models, api
from odoo.exceptions import UserError

from odoo import models, fields, api
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_confirm(self):
        """Override MO confirmation to replace generic components with physical substitutes."""
        res = super().action_confirm()

        for mo in self:
            for move in mo.move_raw_ids:
                product_template = move.product_id.product_tmpl_id

                # Check if it's a generic product
                # if not product_template.is_generic:
                #     continue

                # Get physical substitutes (One2many relation)
                physical_salts = product_template.physical_salts_ids

                if not physical_salts:
                    continue  # or raise error

                qty_to_assign = move.product_uom_qty
                assigned_qty = 0.0

                # Loop through substitutes (linked via substitute_product_id)
                for salt in physical_salts:
                    substitute_template = salt.substitute_product_id

                    if not substitute_template:
                        continue

                    for variant in substitute_template.product_variant_ids:
                        # Get stock quants based on FIFO (by in_date)
                        quants = self.env['stock.quant'].search([
                            ('product_id', '=', variant.id),
                            ('quantity', '>', 0),
                            ('location_id', 'child_of', mo.location_src_id.id)
                        ], order='in_date asc')

                        for quant in quants:
                            if assigned_qty >= qty_to_assign:
                                break

                            available_qty = quant.quantity
                            qty_to_take = min(available_qty, qty_to_assign - assigned_qty)

                            # Create new move using the substitute product
                            new_move = self.env['stock.move'].create({
                                'name': f"{variant.display_name} (substitute for {product_template.name})",
                                'product_id': variant.id,
                                'product_uom_qty': qty_to_take,
                                'product_uom': variant.uom_id.id,
                                'location_id': move.location_id.id,
                                'location_dest_id': move.location_dest_id.id,
                                'picking_type_id': mo.picking_type_id.id,
                                'raw_material_production_id': mo.id,
                                'company_id': mo.company_id.id,
                                'origin': mo.name,
                            })

                            new_move._action_confirm()
                            new_move._action_assign()

                            assigned_qty += qty_to_take

                    if assigned_qty >= qty_to_assign:
                        break

                if assigned_qty < qty_to_assign:
                    raise UserError(
                        f"Not enough stock of substitutes for generic product '{product_template.name}'. "
                        f"Needed: {qty_to_assign}, Assigned: {assigned_qty}"
                    )

                # Remove original generic move
                move.unlink()

        return res


# class MrpProduction(models.Model):
#     _inherit = 'mrp.production'
#
#     def action_confirm(self):
#         """Override MO confirmation to replace generic components with physical substitutes."""
#         res = super().action_confirm()
#
#         for mo in self:
#             for move in mo.move_raw_ids:
#                 product_template = move.product_id.product_tmpl_id
#                 generic_product = product_template.generic_salt_id or product_template
#
#                 # Search for physical products linked to the generic product
#                 physical_templates = generic_product
#                 # physical_templates = self.env['product.template'].search([
#                 #     ('generic_salt_id', '=', generic_product.id)
#                 # ])
#
#                 if not physical_templates:
#                     # No substitutes found, skip or raise error
#                     continue
#
#                 qty_to_assign = move.product_uom_qty
#                 assigned_qty = 0.0
#
#                 for tmpl in physical_templates:
#                     for variant in tmpl.product_variant_ids:
#                         # Find stock quants with positive qty in MO source location or children
#                         quants = self.env['stock.quant'].search([
#                             ('product_id', '=', variant.id),
#                             ('quantity', '>', 0),
#                             ('location_id', 'child_of', mo.location_src_id.id)
#                         ], order='in_date asc')
#
#                         if not quants:
#                             # No stock for this variant - continue to next
#                             continue
#
#                         for quant in quants:
#                             if assigned_qty >= qty_to_assign:
#                                 break
#
#                             available_qty = quant.quantity
#                             qty_to_take = min(available_qty, qty_to_assign - assigned_qty)
#
#                             # Create stock move for this physical variant
#                             new_move = self.env['stock.move'].create({
#                                 'name': f"{variant.display_name} (from {generic_product.name})",
#                                 'product_id': variant.id,
#                                 'product_uom_qty': qty_to_take,
#                                 'product_uom': variant.uom_id.id,
#                                 'location_id': move.location_id.id,
#                                 'location_dest_id': move.location_dest_id.id,
#                                 'picking_type_id': mo.picking_type_id.id,
#                                 'raw_material_production_id': mo.id,
#                                 'company_id': mo.company_id.id,
#                                 'origin': mo.name,
#                             })
#
#                             # Confirm and assign the move to reserve stock immediately
#                             new_move._action_confirm()
#                             new_move._action_assign()
#
#                             assigned_qty += qty_to_take
#
#                 if assigned_qty < qty_to_assign:
#                     raise UserError(
#                         f"Not enough stock of physical substitutes for generic product '{generic_product.name}'. "
#                         f"Needed: {qty_to_assign}, assigned: {assigned_qty}"
#                     )
#
#                 # Remove the original generic product move
#                 move.unlink()
#
#         return res
