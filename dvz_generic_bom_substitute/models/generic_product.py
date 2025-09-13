from odoo import models, fields, api

class GenericProduct(models.Model):
    _name = 'generic.product'

    name = fields.Char(string="Substitute Name")  # Optional: for visibility
    generic_salt_id = fields.Many2one(
        'product.template',
        string="Generic Product",
        help="Link this product as a substitute of a generic product."
    )

    # Optional: link to actual product
    substitute_product_id = fields.Many2one(
        'product.template',
        string="Substitute Product",
        help="Actual product that acts as a substitute."
    )

    onhand_qty = fields.Float(
        string="On Hand Qty",
        compute="_compute_onhand_qty",
        store=False,
        help="Total on-hand quantity for this substitute product."
    )

    @api.depends('substitute_product_id')
    def _compute_onhand_qty(self):
        for record in self:
            qty = 0.0
            if record.substitute_product_id:
                for variant in record.substitute_product_id.product_variant_ids:
                    qty += variant.qty_available  # Sum across all variants
            record.onhand_qty = qty
