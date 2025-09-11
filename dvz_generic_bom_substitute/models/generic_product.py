from odoo import models, fields

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
