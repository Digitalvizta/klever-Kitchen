from odoo import models, fields, api

class GenericProduct(models.Model):
    _name = 'generic.product'

    name = fields.Char(string="Substitute Name")  # Optional: for visibility
    generic_salt_id = fields.Many2one(
        'product.template',
        string="Generic Product",
        help="Link this product as a substitute of a generic product."
    )

    # Optional: link to actual product
    substitute_product_id = fields.Many2one(
        'product.template',
        string="Substitute Product",
        domain=[('purchase_ok', '=', True)],
        help="Actual product that acts as a substitute."
    )

    onhand_qty = fields.Float(
        string="On Hand Qty",
        compute="_compute_onhand_qty",
        store=False,
        help="Total on-hand quantity for this substitute product."
    )

    vendor_id = fields.Many2one(
        'res.partner',
        string="Vendor",
        help="Vendor who supplies this substitute product."
    )

    vendor_code = fields.Char(
        string="Vendor Product Code",
        help="Product code used by the vendor."
    )

    @api.depends('substitute_product_id')
    def _compute_onhand_qty(self):
        for record in self:
            qty = 0.0
            if record.substitute_product_id:
                for variant in record.substitute_product_id.product_variant_ids:
                    qty += variant.qty_available  # Sum across all variants
            record.onhand_qty = qty

    @api.onchange('vendor_id')
    def _onchange_vendor_id(self):
        if self.vendor_id:
            supplier_infos = self.env['product.supplierinfo'].search([('partner_id', '=', self.vendor_id.id)])
            product_ids = supplier_infos.mapped('product_tmpl_id').ids
            products_with_vendor = self.env['product.template'].browse(product_ids).filtered(lambda p: p.purchase_ok)
            return {
                'domain': {
                    'substitute_product_id': [('id', 'in', products_with_vendor.ids)]
                }
            }
        else:
            # No vendor selected — no products should be visible
            return {
                'domain': {
                    'substitute_product_id': [('id', '=', False)]
                }
            }

