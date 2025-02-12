from odoo import models, fields

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    # Add your custom field here
    schedule_delivery_date = fields.Date(string="Schedule Delivery Date")
