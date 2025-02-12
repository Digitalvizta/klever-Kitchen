# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class Sector(models.Model):
    _name = 'sh.sector'
    _description = "Sector"
    _order = 'sequence, id'

    name = fields.Char(required=True)
    from_time = fields.Float(string="From", required=True)
    to_time = fields.Float(string="To", required=True)
    sequence = fields.Integer()
