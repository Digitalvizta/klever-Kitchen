from odoo import models, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _apply_card_payment_tax(self, vals_list):
        """
        Applies 5% tax to order lines if any payment method is of type 'card'.
        """
        tax_5_percent = self.env['account.tax'].search([
            ('amount', '=', 5),
            ('type_tax_use', '=', 'sale'),
        ], limit=1)

        for vals in vals_list:
            is_card_payment = False
            payment_lines = vals.get('payment_ids', [])

            for payment_line in payment_lines:
                # Format: [0, 0, {payment_line_data}]
                if (
                    isinstance(payment_line, (list, tuple))
                    and len(payment_line) == 3
                    and isinstance(payment_line[2], dict)
                ):
                    payment_data = payment_line[2]
                    method_id = payment_data.get('payment_method_id')
                    if method_id:
                        method = self.env['pos.payment.method'].browse(method_id)
                        if method and 'card' in (method.name or '').lower():
                            is_card_payment = True
                            break

            if is_card_payment and 'lines' in vals:
                for line in vals['lines']:
                    if len(line) == 3 and isinstance(line[2], dict):
                        line_data = line[2]
                        if tax_5_percent:
                            line_data['tax_ids'] = [(6, 0, [tax_5_percent.id])]

    @api.model_create_multi
    def create(self, vals_list):
        self._apply_card_payment_tax(vals_list)
        return super().create(vals_list)

    def write(self, vals):
        # Apply tax only during write when payment_ids or lines are involved
        self._apply_card_payment_tax([vals])
        return super().write(vals)
