# models/sale_order.py

from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pickup_date = fields.Datetime(string='Pick Up Date')
    fulfill_order_date = fields.Datetime(string='Fulfill Order')
    po_no = fields.Char(string='PO No.')
    bol = fields.Char(string='BOL (Bill of Lading)')
    lot_no = fields.Char(string='Lot No.')
