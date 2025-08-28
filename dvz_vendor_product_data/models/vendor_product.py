from odoo import models, fields


class VendorProduct(models.Model):
    _name = 'vendor.product'
    _description = 'Vendor Product'
    _rec_name = 'product_name'

    product_id = fields.Many2one('product.product', string='Product Variant', required=False)
    product_tmpl_id = fields.Many2one('product.template', string='Product', required=False)
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True, ondelete='cascade')

    product_name = fields.Char(string='Vendor Product Name')
    product_code = fields.Char(string='Vendor Product Code')

    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')

    sequence = fields.Integer(string='Sequence', default=10)
    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    min_qty = fields.Float(string='Minimum Quantity', default=0.0)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure')
    price = fields.Float(string='Price')
    discount = fields.Float(string='Discount (%)', default=0.0)
    delay = fields.Integer(string='Delivery Lead Time (Days)', default=1)
