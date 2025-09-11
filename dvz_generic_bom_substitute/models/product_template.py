from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_generic = fields.Boolean(string="Is Generic Product", default=False)

    physical_salts_ids = fields.One2many(
        'generic.product',
        'generic_salt_id',
        string="Substitute Products",
        help="Actual inventory products that can be used instead of this generic product."
    )
