from odoo import models, fields

class VendorMaster(models.Model):
    _name = 'vendor.master'
    _description = 'Vendor Master'

    vendor_name = fields.Many2one('res.partner', string='Vendor', required=True, domain="[('is_vendor', '=', True)]")
    product_lines = fields.One2many('vendor.product', 'vendor_id', string='Products')


class VendorProduct(models.Model):
    _name = 'vendor.product'
    _description = 'Vendor Product'

    product_id = fields.Many2one('product.template', string='Product', required=True)
    vendor_id = fields.Many2one('vendor.master', string='Vendor', required=True, ondelete='cascade')


# Independent mapping model (if needed separately)
class VendorProductMapping(models.Model):
    _name = 'vendor.product.mapping'
    _description = 'Vendor & Product Mapping'
    _rec_name = 'product_name'

    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True, domain="[('is_vendor', '=', 1)]")
    vendor_product_id = fields.Many2one('product.template', string='Product', required=True)
    product_name = fields.Char(string='Vendor Product',help='Custom reference code for vendor-product mapping')
