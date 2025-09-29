from odoo import models, fields

class ProductCategoryType(models.Model):
    _name = "product.category.type"
    _description = "Product Category Type"
    _inherit = ["mail.thread", "mail.activity.mixin"]  # enables chatter

    name = fields.Char(
        string="Name",
        required=True,
        tracking=True
    )
    description = fields.Text(string="Description")
