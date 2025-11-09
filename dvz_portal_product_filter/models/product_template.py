from odoo import models, api, fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    allowed_customer_ids = fields.Many2many(
        'res.partner',
        string="Allowed Customers",
        help="Only selected customers can view this product on the portal."
    )

    @api.model
    def _website_search(self, domain, search, **kwargs):
        partner = self.env.user.partner_id
        if partner and not self.env.user.has_group('base.group_system'):
            domain += [('allowed_customer_ids', 'in', [partner.id])]
        return super()._website_search(domain, search, **kwargs)
