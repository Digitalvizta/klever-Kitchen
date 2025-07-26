# models/sale_order.py

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    actual_ship_date = fields.Datetime(
        string='Actual Ship Date',
        help='After completion, enter the date the order was actually picked up or delivered.',
        required=False
    )
    pickup_week_number = fields.Char(string='Week Number', compute='_compute_week_number', store=True)

    @api.depends('pickup_delivery_datetime')
    def _compute_week_number(self):
        for order in self:
            if order.pickup_delivery_datetime:
                order.pickup_week_number = f"Week {order.pickup_delivery_datetime.isocalendar()[1]}"
            else:
                order.pickup_week_number = ''
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

    @api.constrains('pickup_delivery_datetime', 'actual_ship_date', 'fulfill_order_date', 'schedule_delivery_date')
    def _check_dates_after_fulfill(self):
        for order in self:
            if order.fulfill_order_date:
                if order.pickup_delivery_datetime and order.pickup_delivery_datetime < order.fulfill_order_date:
                    raise ValidationError("Pick Up / Delivery Date & Time must be after Date of Order.")
                if order.actual_ship_date and order.actual_ship_date < order.fulfill_order_date:
                    raise ValidationError("Actual Ship Date must be after Date of Order.")


