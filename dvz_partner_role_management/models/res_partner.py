from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_employee = fields.Boolean("Is Employee")

    @api.constrains('is_customer', 'is_vendor', 'is_both', 'is_employee')
    def _check_single_selection(self):
        for rec in self:
            selected = sum([
                1 if rec.is_customer else 0,
                1 if rec.is_vendor else 0,
                1 if rec.is_both else 0,
                1 if rec.is_employee else 0,
            ])
            if selected > 1:
                raise ValidationError("You can only select one: Customer, Vendor, Both, or Employee.")

    @api.onchange('is_customer', 'is_vendor', 'is_both', 'is_employee')
    def _onchange_selection(self):
        """Reset other fields if one is selected"""
        for rec in self:
            if rec.is_customer:
                rec.is_vendor = rec.is_both = rec.is_employee = False
            elif rec.is_vendor:
                rec.is_customer = rec.is_both = rec.is_employee = False
            elif rec.is_both:
                rec.is_customer = rec.is_vendor = rec.is_employee = False
            elif rec.is_employee:
                rec.is_customer = rec.is_vendor = rec.is_both = False
