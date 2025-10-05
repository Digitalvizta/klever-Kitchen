from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = "product.category"

    # parent_category_id = fields.Many2one(
    parent_category_id = fields.Many2many(
        "product.parent.category",
        string="Parent Category",
        help="Select the main category for this category"
    )

    main_category_id = fields.Many2one(
        "product.category.type",
        string="Main Category"
    )
