from odoo import models, fields, api

class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    product_name_ref = fields.Many2one('vendor.product', string="Product Name")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.product_name_ref = False

    @api.onchange('product_name_ref')
    def _onchange_product_name_ref(self):
        if self.product_name_ref:
            self.product_name = self.product_name_ref.product_name
