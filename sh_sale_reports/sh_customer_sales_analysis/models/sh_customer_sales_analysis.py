# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class SalesAnalysisOrderReport(models.Model):
    _name = 'sh.customer.sales.analysis.order'
    _description = 'Customer Analysis Order'

    name = fields.Char(string='Order Number')
    order_date = fields.Date()
    user_id = fields.Many2one(
        'res.users', string='Salesperson')
    sh_partner_id = fields.Many2one(
        'res.partner', string='Customer')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id')
    sales_amount = fields.Monetary()
    amount_paid = fields.Monetary()
    balance = fields.Monetary()


class SalesAnalysisProductReport(models.Model):
    _name = 'sh.customer.sales.analysis.product'
    _description = 'Customer Analysis Product'

    name = fields.Char(string='Order Number')
    order_date = fields.Date(string='Date')
    sh_partner_id = fields.Many2one(
        'res.partner', string='Customer')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id')
    sh_product_id = fields.Many2one(
        comodel_name='product.product', string='Product')
    price = fields.Monetary()
    quantity = fields.Float()
    discount = fields.Float(string="Discount (%)")
    tax = fields.Float()
    subtotal = fields.Monetary()
