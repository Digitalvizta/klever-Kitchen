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

    # product_category_type = fields.Selection([
    #     ('mfg', 'MFG'),
    #     ('fg', 'FG'),
    #     ('vd', 'VD'),
    #     ('rm', 'RM'),
    #     ('sfg', 'SFG'),
    # ], string="Product Category Type", required=True)
    #
    # auto_sequence_code = fields.Char(string="Auto Sequence Code", readonly=False, copy=False)
    #
    # @api.onchange('product_category_type')
    # def _onchange_product_category_type(self):
    #     if self.product_category_type:
    #         auto_sequence_code = self.env['ir.sequence'].next_by_code(f'{self.product_category_type}_sequence')
    #         self.auto_sequence_code = auto_sequence_code



class ProductProduct(models.Model):
    _inherit = 'product.product'

    rm_vendor_product_ids = fields.Many2many(
        'product.product',
        string="RM Vendor Products",
        compute="_compute_rm_vendor_data",
        store=False
    )

    rm_onhand_qty = fields.Float(
        string="RM On Hand Qty (Sum)",
        compute="_compute_rm_vendor_data",
        store=False,
        help="Sum of on-hand quantities of all substitute products linked via physical_salts_ids."
    )

    rm_vendor_qty_sum = fields.Float(
        string="RM Vendor Product Qty Sum",
        compute="_compute_rm_vendor_data",
        store=False
    )

    @api.depends('product_tmpl_id.physical_salts_ids.substitute_product_id')
    def _compute_rm_vendor_data(self):
        """
        Compute RM-related quantities and products using the
        physical_salts_ids.one2many on product.template.
        """
        for product in self:
            tmpl = product.product_tmpl_id
            vendor_products = self.env['product.product']

            total_qty = 0.0

            # if tmpl.physical_salts_ids:
            for line in tmpl.physical_salts_ids:
                if line.substitute_product_id:
                    # get all variants of that substitute product
                    variants = line.substitute_product_id.product_variant_ids
                    vendor_products |= variants
                    total_qty += sum(variants.mapped('qty_available'))

            product.rm_vendor_product_ids = vendor_products
            product.rm_onhand_qty = total_qty
            product.rm_vendor_qty_sum = total_qty
