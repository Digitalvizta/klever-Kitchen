from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_customer = fields.Boolean("Is Customer")
    is_vendor = fields.Boolean("Is Vendor")
    is_both = fields.Boolean("Is Customer & Vendor")
