# -*- coding: utf-8 -*-

# models/pos_order.py
from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def _order_fields(self, ui_order):
        res = super()._order_fields(ui_order)

        # Check for card journal in payment lines
        is_card_payment = any(
            payment.get('journal_type') == 'card'
            for payment in ui_order.get('payment_lines', [])
        )

        if is_card_payment:
            # Add 5% tax to order lines (backend safety)
            tax_5_percent = self.env['account.tax'].search([('amount', '=', 5), ('type_tax_use', '=', 'sale')], limit=1)
            if tax_5_percent:
                for line in res['lines']:
                    line[2]['tax_ids'] = [(6, 0, [tax_5_percent.id])]

        return res


