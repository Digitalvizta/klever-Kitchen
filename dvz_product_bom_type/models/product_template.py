from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_bom = fields.Boolean("Is BOM")

    @api.constrains('sale_ok', 'purchase_ok', 'is_bom')
    def _check_single_flag_selected(self):
        for rec in self:
            selected_flags = sum([
                1 if rec.sale_ok else 0,
                1 if rec.purchase_ok else 0,
                1 if rec.is_bom else 0,
            ])
            if selected_flags > 1:
                raise ValidationError("Only one of Sale, Purchase, or BOM can be selected.")

    @api.onchange('sale_ok', 'purchase_ok', 'is_bom')
    def _onchange_flags(self):
        for rec in self:
            if rec.sale_ok:
                rec.purchase_ok = False
                rec.is_bom = False
            elif rec.purchase_ok:
                rec.sale_ok = False
                rec.is_bom = False
            elif rec.is_bom:
                rec.sale_ok = False
                rec.purchase_ok = False
