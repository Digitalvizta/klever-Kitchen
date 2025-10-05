from odoo import models, fields

class ProductParentCategory(models.Model):
    _name = "product.parent.category"
    _description = "Product Parent Category"
    _inherit = ["mail.thread", "mail.activity.mixin"]  # enables chatter

    name = fields.Char(
        string="Name",
        required=True,
        tracking=True
    )
    description = fields.Text(string="Description")

    # product_category_type = fields.Many2one('product.category.type', string="Main Category", required=True)
    product_category_type = fields.Many2many('product.category.type', string="Main Category", required=True)

