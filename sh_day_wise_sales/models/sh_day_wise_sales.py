# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class SalesDayWiseReport(models.Model):
    _name = 'sh.sales.day.wise.report'
    _description = 'Sales Wise Daily Report'

    name = fields.Many2one(
        comodel_name='product.product', string='Product Name')

    monday = fields.Integer()
    tuesday = fields.Integer()
    wednesday = fields.Integer()
    thursday = fields.Integer()
    friday = fields.Integer()
    saturday = fields.Integer()
    sunday = fields.Integer()
    total = fields.Integer()
