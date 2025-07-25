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
    pickup_delivery_date = fields.Datetime(string='Pick Up /  Delivery', required=False)
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
                # if order.schedule_delivery_date and order.schedule_delivery_date < order.fulfill_order_date:
                #     raise ValidationError("Production Date must be after Date of Order.")

# def action_confirm(self):
    #     res = super().action_confirm()
    #
    #     for order in self:
    #         child_order = order.mrp_production_ids[0]
    #         for mo in order.mrp_production_ids:
    #             if mo:
    #                 mo.production_date = order.schedule_delivery_date
    #
    #                 for raw in mo.move_raw_ids:
    #                     raw.created_production_id.production_date = order.schedule_delivery_date
    #                 for raw in mo.move_finished_ids:
    #                     raw.created_production_id.production_date = order.schedule_delivery_date
    #                 for raw in mo.move_dest_ids:
    #                     cc = raw
    #                     ddd = cc
    #                     raw.created_production_id.production_date = order.schedule_delivery_date
    #     return res

