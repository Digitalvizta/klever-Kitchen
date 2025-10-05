from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = "product.category"

    parent_category_id = fields.Many2one(
        "product.parent.category",
        string="Main Category",
        help="Select the main category for this category"
    )
