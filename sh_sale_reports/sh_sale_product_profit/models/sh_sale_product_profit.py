# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class SalesProductProfitReport(models.Model):
    _name = 'sh.sale.product.profit'
    _description = 'Sales Product Profit'

    name = fields.Char(string='Order Number')
    date_order = fields.Date(string='Order Date')
    product_id = fields.Many2one(
        'product.product', string='Product', )
    qty = fields.Float(string='Quantity')
    profit = fields.Float()
    margin = fields.Float(string="Margin (%)")
    sh_partner_id = fields.Many2one(
        'res.partner', string='Customer')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id')
    cost = fields.Monetary()
    sale_price = fields.Monetary()
