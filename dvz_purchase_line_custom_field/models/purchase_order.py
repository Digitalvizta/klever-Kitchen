from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    x_custom_field = fields.Char(string='Custom Info')

    vendor_id = fields.Many2one(
        related='order_id.partner_id',
        string='Vendor',
        store=True,
        readonly=True
    )

    vendor_product_mapping_id = fields.Many2one(
        'vendor.product.mapping',
        string='Vendor Product',
        domain="[('vendor_id', '=', vendor_id)]",
        help='Link to vendor-product reference mapping',
    )


    @api.onchange('vendor_product_mapping_id')
    def _onchange_vendor_product_mapping(self):
        if self.vendor_product_mapping_id:
            product_template = self.vendor_product_mapping_id.vendor_product_id
            if product_template and product_template.product_variant_ids:
                # Assign the first product variant to product_id
                self.product_id = product_template.product_variant_ids[0]





