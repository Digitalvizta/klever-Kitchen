from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    supplierinfo_count = fields.Integer(
        compute='_compute_supplierinfo_count',
        string='Supplier Info Count'
    )

    def _compute_supplierinfo_count(self):
        for partner in self:
            count = self.env['product.supplierinfo'].search_count([('partner_id', '=', partner.id)])
            partner.supplierinfo_count = count

    def open_supplierinfos(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Supplier Info',
            'res_model': 'product.supplierinfo',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }
