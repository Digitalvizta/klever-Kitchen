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

    actual_ship_week_number = fields.Char(
        string='Week Number',
        compute='_compute_actual_ship_week_number',
        store=True
    )

    @api.depends('actual_ship_date')
    def _compute_actual_ship_week_number(self):
        for order in self:
            if order.actual_ship_date:
                order.actual_ship_week_number = f"Week {order.actual_ship_date.isocalendar()[1]}"
            else:
                order.actual_ship_week_number = ''

    pickup_week_number = fields.Char(string='Week Number', compute='_compute_week_number', store=True)

    @api.depends('pickup_delivery_datetime')
    def _compute_week_number(self):
        for order in self:
            if order.pickup_delivery_datetime:
                order.pickup_week_number = f"Week {order.pickup_delivery_datetime.isocalendar()[1]}"
            else:
                order.pickup_week_number = ''

    fulfill_order_date = fields.Datetime(string='Date of Order')

    fulfill_order_week_number = fields.Char(
        string='Week Number',
        compute='_compute_fulfill_order_week_number',
        store=True
    )

    @api.depends('fulfill_order_date')
    def _compute_fulfill_order_week_number(self):
        for record in self:
            if record.fulfill_order_date:
                record.fulfill_order_week_number = f"Week {record.fulfill_order_date.isocalendar()[1]}"
            else:
                record.fulfill_order_week_number = ''

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

    schedule_delivery_week_number = fields.Char(
        string='Week Number',
        compute='_compute_schedule_delivery_week_number',
        store=True
    )

    @api.depends('schedule_delivery_date')
    def _compute_schedule_delivery_week_number(self):
        for record in self:
            if record.schedule_delivery_date:
                record.schedule_delivery_week_number = f"Week {record.schedule_delivery_date.isocalendar()[1]}"
            else:
                record.schedule_delivery_week_number = ''

    date_order_week_number = fields.Char(
        string='Week Number',
        compute='_compute_date_order_week_number',
        store=True
    )

    @api.depends('date_order')
    def _compute_date_order_week_number(self):
        for record in self:
            if record.date_order:
                record.date_order_week_number = f"Week {record.date_order.isocalendar()[1]}"
            else:
                record.date_order_week_number = ''


