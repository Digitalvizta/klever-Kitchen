from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_generic = fields.Boolean(string="Is Generic Product", default=False)

    physical_salts_ids = fields.One2many(
        'generic.product',
        'generic_salt_id',
        string="Substitute Products",
        help="Actual inventory products that can be used instead of this generic product."
    )

    product_category_type = fields.Selection([
        ('mfg', 'MFG'),
        ('fg', 'FG'),
        ('vd', 'VD'),
        ('rm', 'RM'),
        ('sfg', 'SFG'),
    ], string="Product Category Type", required=True)

    auto_sequence_code = fields.Char(string="Auto Sequence Code", readonly=False, copy=False)

    @api.onchange('product_category_type')
    def _onchange_product_category_type(self):
        if self.product_category_type:
            auto_sequence_code = self.env['ir.sequence'].next_by_code(f'{self.product_category_type}_sequence')
            self.auto_sequence_code = auto_sequence_code