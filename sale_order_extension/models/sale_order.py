# models/sale_order.py

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    actual_ship_date = fields.Datetime(
        string='Actual Ship Date',
        help='After completion, enter the date the order was actually picked up or delivered.',
        required=True
    )
    pickup_delivery_date = fields.Datetime(string='Pick Up /  Delivery', required=True)
    fulfill_order_date = fields.Datetime(string='Date of Order')
    po_no = fields.Char(string='PO No.')
    bol = fields.Char(string='BOL (Bill of Lading)',)
    lot_no = fields.Char(string='Lot No.', )


    pickup_delivery = fields.Selection([
        ('pickup', 'Pick Up'),
        ('delivery', 'Delivery')
    ], string='Pick Up / Delivery', required=True, default='pickup')

    pickup_delivery_datetime = fields.Datetime(
        string='Pick Up / Delivery Date & Time',
        required=True
    )

    def action_confirm(self):
        res = super().action_confirm()

        for order in self:
            for mo in order.mrp_production_ids:

                if mo:
                    mo.production_date = order.schedule_delivery_date

        return res

