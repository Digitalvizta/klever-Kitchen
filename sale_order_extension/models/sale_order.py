# models/sale_order.py

from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pickup_date = fields.Datetime(string='Actual Ship Date')
    pickup_delivery_date = fields.Datetime(string='Pick Up /  Delivery')
    fulfill_order_date = fields.Datetime(string='Order Order')
    po_no = fields.Char(string='PO No.')
    bol = fields.Char(string='BOL (Bill of Lading)')
    lot_no = fields.Char(string='Lot No.')
