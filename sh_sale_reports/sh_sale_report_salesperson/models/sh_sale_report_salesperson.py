# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class SalesInvoiceSummaryReport(models.Model):
    _name = 'sh.sale.report.salesperson'
    _description = 'Sales Report By Saleperson'

    name = fields.Char(string='Order Number')
    date_order = fields.Datetime(string='Order Date')
    sh_partner_id = fields.Many2one(
        'res.partner', string='Customer')
    sh_user_id = fields.Many2one(
        'res.users', string='Sales Person')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id')
    total = fields.Monetary()
    paid_amount = fields.Monetary(string="Amount Invoiced")
    due_amount = fields.Monetary(string="Amount Due")
