from odoo import models, fields, api

class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    def _create_vendor_product_mapping(self):
        for supplierinfo in self:
            vendor = supplierinfo.partner_id
            product = supplierinfo.product_tmpl_id
            product_name = supplierinfo.product_name

            if vendor and product:
                mapping = self.env['vendor.product.mapping'].search([
                    ('vendor_id', '=', vendor.id),
                    ('vendor_product_id', '=', product.id)
                ], limit=1)

                # if not mapping:
            self.env['vendor.product.mapping'].create({
                'vendor_id': vendor.id,
                'vendor_product_id': product.id,
                'product_name': product_name
            })
                # else:
                #     mapping.write({
                #         'vendor_id': vendor.id,
                #         'vendor_product_id': product.id,
                #         'product_name': product_name  # or 'reference_code': product_name
                #     })

    def create(self, vals_list):
        records = super().create(vals_list)
        records._create_vendor_product_mapping()
        return records

    def write(self, vals):
        result = super().write(vals)
        if 'product_name' in vals:
            self._create_vendor_product_mapping()
        return result
