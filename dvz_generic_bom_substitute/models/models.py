# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class dvz_generic_bom_substitute(models.Model):
#     _name = 'dvz_generic_bom_substitute.dvz_generic_bom_substitute'
#     _description = 'dvz_generic_bom_substitute.dvz_generic_bom_substitute'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

