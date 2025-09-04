from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    vendor_id = fields.Many2one(
        related='order_id.partner_id',
        string='Vendor',
        store=True,
        readonly=True
    )

    vendor_product = fields.Many2one(
        'vendor.product',
        string='Vendor Product',
        domain="[('vendor_id', '=', vendor_id)]",
        help='Link to vendor-product reference mapping',
    )
