from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    allowed_user_ids = fields.Many2many(
        'res.users',
        string="Allowed Portal Users",
        domain=[('share', '=', True)],
        help="Only selected portal users can view this product on the portal."
    )

    @api.model
    def _website_search(self, domain, search, **kwargs):
        user = self.env.user
        if user and not user.has_group('base.group_system'):
            domain += [('allowed_user_ids', 'in', [user.id])]
        return super()._website_search(domain, search, **kwargs)
