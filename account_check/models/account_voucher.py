# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.tools import float_is_zero
import logging
import json
from datetime import datetime

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    """Extend account.move to handle check-based outstanding payments"""
    _inherit = 'account.move'

    def _compute_payments_widget_to_reconcile_info(self):
        """Compute outstanding credits/debits for invoices with check payments"""
        for move in self:
            move.invoice_outstanding_credits_debits_widget = json.dumps(False)
            move.invoice_has_outstanding = False

            if move.state != 'posted' or move.payment_state not in ('not_paid', 'partial') or not move.is_invoice(include_receipts=True):
                continue

            pay_term_lines = move.line_ids.filtered(
                lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')
            )

            domain = [
                ('account_id', 'in', pay_term_lines.account_id.ids),
                ('move_id.state', '=', 'posted'),
                ('partner_id', '=', move.commercial_partner_id.id),
                ('reconciled', '=', False),
                '|', ('amount_residual', '!=', 0.0), ('amount_residual_currency', '!=', 0.0),
            ]

            payments_widget_vals = {'outstanding': True, 'content': [], 'move_id': move.id}
            payments_widget_vals['title'] = _('Outstanding credits') if move.is_inbound() else _('Outstanding debits')
            domain.append(('balance', '<' if move.is_inbound() else '>', 0.0))

            for line in self.env['account.move.line'].search(domain):
                checks_amount = 0.0
                if line.journal_id.payment_subtype:
                    checks = (
                        line.payment_id.received_third_check_ids
                        if line.journal_id.payment_subtype == 'third_check'
                        else line.payment_id.issued_check_ids
                    )
                    for check in checks:
                        checks_amount += check.amount if check.state in ('deposited', 'debited') else 0.0
                    if float_is_zero(checks_amount, precision_digits=move.currency_id.decimal_places):
                        continue

                amount = (
                    abs(line.amount_residual_currency)
                    if line.currency_id == move.currency_id
                    else move.company_currency_id._convert(
                        abs(line.amount_residual),
                        move.currency_id,
                        move.company_id,
                        line.date or fields.Date.today()
                    )
                )
                amount = checks_amount if line.journal_id.payment_subtype else amount
                if float_is_zero(amount, precision_digits=move.currency_id.decimal_places):
                    continue

                payments_widget_vals['content'].append({
                    'journal_name': line.ref or line.move_id.name,
                    'amount': amount,
                    'currency': move.currency_id.symbol,
                    'id': line.id,
                    'move_id': line.move_id.id,
                    'position': move.currency_id.position,
                    'digits': [69, move.currency_id.decimal_places],
                    'payment_date': fields.Date.to_string(line.date),
                })

            if not payments_widget_vals['content']:
                continue

            move.invoice_outstanding_credits_debits_widget = json.dumps(payments_widget_vals)
            total_amount = sum(content['amount'] for content in payments_widget_vals['content'])
            move.invoice_has_outstanding = bool(total_amount > 0.0)

class AccountPayment(models.Model):
    """Extend account.payment to support check-based payments"""
    _inherit = 'account.payment'

    payment_subtype = fields.Selection(
        related='journal_id.payment_subtype',
        string='Payment Subtype',
        store=True,
        help="Payment subtype inherited from the journal"
    )
    received_third_check_ids = fields.One2many(
        comodel_name='account.check',
        inverse_name='voucher_id',
        string='Third Checks',
        domain=[('type', '=', 'third_check')],
        context={'default_type': 'third_check', 'from_voucher': True},
        help="Third-party checks received for this payment"
    )
    issued_check_ids = fields.One2many(
        comodel_name='account.check',
        inverse_name='voucher_id',
        string='Issued Checks',
        domain=[('type', '=', 'issue_check')],
        context={'default_type': 'issue_check', 'from_voucher': True},
        help="Checks issued for this payment"
    )
    delivered_third_check_ids = fields.One2many(
        comodel_name='account.check',
        inverse_name='third_handed_voucher_id',
        string='Delivered Third Checks',
        domain=[('type', '=', 'third_check')],
        context={'from_voucher': True},
        help="Third-party checks delivered for this payment"
    )
    checks_amount = fields.Monetary(
        string='Checks Amount',
        compute='_compute_checks_amount',
        digits='Account',
        help="Total amount paid with checks"
    )
    net_amount = fields.Monetary(
        string='Net Amount',
        currency_field='currency_id',
        digits='Account',
        default=0.0,
        help="Amount paid with journal method"
    )
    paylines_amount = fields.Monetary(
        string='Paylines Amount',
        currency_field='currency_id',
        compute='_compute_paylines_amount',
        digits='Account',
        help="Amount paid with paylines (checks, withholdings, etc.)"
    )
    amount = fields.Monetary(
        string='Total Amount',
        currency_field='currency_id',
        compute='_compute_amount',
        inverse='_inverse_amount',
        store=True,
        digits='Account',
        help="Total amount paid"
    )
    amount_readonly = fields.Monetary(
        string='Total Amount (Readonly)',
        currency_field='currency_id',
        related='amount',
        digits='Account',
        help="Readonly view of the total amount paid"
    )
    dummy_journal_id = fields.Many2one(
        comodel_name='account.journal',
        related='journal_id',
        string='Dummy Journal',
        help="Technical field for journal onchange methods"
    )

    def _get_valid_liquidity_accounts(self):
        """Extend valid liquidity accounts to include check-related accounts"""
        valid_accounts = super()._get_valid_liquidity_accounts()
        journal_accounts = self.env['account.account']
        for account in [self.journal_id.under_collection_acc_id, self.journal_id.handed_acc_id, self.journal_id.long_term_account]:
            if account:
                journal_accounts |= account
        return valid_accounts | journal_accounts

    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        """Reset check-related fields when journal changes"""
        if self.journal_id.payment_subtype in ('issue_check', 'third_check'):
            self.net_amount = 0.0
        self.delivered_third_check_ids = False
        self.issued_check_ids = False
        self.received_third_check_ids = False

    @api.depends('received_third_check_ids', 'delivered_third_check_ids', 'issued_check_ids')
    def _compute_checks_amount(self):
        """Compute total amount from related checks"""
        for payment in self:
            checks_amount = sum(
                check.amount
                for checks in [
                    payment.received_third_check_ids,
                    payment.delivered_third_check_ids,
                    payment.issued_check_ids
                ]
                for check in checks
            )
            payment.checks_amount = checks_amount
            payment.net_amount = checks_amount
            payment._compute_paylines_amount()
            payment._compute_amount()

    # @api.depends('journal_id', 'payment_type', 'payment_method_line_id')
    # def _compute_outstanding_account_id(self):
    #     """Set outstanding account based on check type and payment date"""
    #     super()._compute_outstanding_account_id()
    #     for payment in self:
    #         if payment.payment_subtype not in ('issue_check', 'third_check'):
    #             continue
    #         current_year_end = fields.Date.today().replace(month=12, day=31)
    #         if payment.payment_type == 'inbound':
    #             payment.outstanding_account_id = payment.journal_id.under_collection_acc_id
    #             if payment.journal_id.long_term_account:
    #                 for check in payment.received_third_check_ids:
    #                     check_date = fields.Date.from_string(check.payment_date)
    #                     if check_date > current_year_end:
    #                         check.long_term_check = True
    #                         payment.outstanding_account_id = payment.journal_id.long_term_account
    #         elif payment.payment_type == 'outbound':
    #             payment.outstanding_account_id = payment.journal_id.handed_acc_id
    #             if payment.journal_id.long_term_account:
    #                 for check in payment.issued_check_ids:
    #                     check_date = fields.Date.from_string(check.payment_date)
    #                     if check_date > current_year_end:
    #                         check.long_term_check = True
    #                         payment.outstanding_account_id = payment.journal_id.long_term_account
    #         else:
    #             payment.outstanding_account_id = False
    #         _logger.debug("Outstanding account set to: %s", payment.outstanding_account_id.name or "None")
    @api.depends('journal_id', 'payment_type', 'payment_method_line_id')
    def _compute_outstanding_account_id(self):
        """Set outstanding account based on check type and payment date"""
        super()._compute_outstanding_account_id()
        for payment in self:
            if payment.payment_subtype not in ('issue_check', 'third_check'):
                continue

            current_year_end = fields.Date.today().replace(month=12, day=31)

            if payment.payment_type == 'inbound':
                payment.outstanding_account_id = payment.journal_id.under_collection_acc_id
                if payment.journal_id.long_term_account:
                    for check in payment.received_third_check_ids:
                        if check.payment_date:  # ✅ only compare if date exists
                            check_date = fields.Date.from_string(check.payment_date)
                            if check_date and check_date > current_year_end:
                                check.long_term_check = True
                                payment.outstanding_account_id = payment.journal_id.long_term_account

            elif payment.payment_type == 'outbound':
                payment.outstanding_account_id = payment.journal_id.handed_acc_id
                if payment.journal_id.long_term_account:
                    for check in payment.issued_check_ids:
                        if check.payment_date:  # ✅ only compare if date exists
                            check_date = fields.Date.from_string(check.payment_date)
                            if check_date and check_date > current_year_end:
                                check.long_term_check = True
                                payment.outstanding_account_id = payment.journal_id.long_term_account

            else:
                payment.outstanding_account_id = False

            _logger.debug("Outstanding account set to: %s", payment.outstanding_account_id.name or "None")

    def action_post(self):
        """Update check states upon posting payment"""
        res = super().action_post()
        for payment in self:
            if payment.payment_type == 'outbound':
                payment.issued_check_ids.write({'state': 'handed'})
                payment.delivered_third_check_ids.write({'state': 'handed'})
            elif payment.payment_type == 'inbound':
                payment.received_third_check_ids.write({'state': 'holding'})
        return res

    @api.depends('net_amount', 'paylines_amount')
    def _compute_amount(self):
        """Compute total amount as sum of net and paylines amounts"""
        for payment in self:
            payment.amount = payment.paylines_amount + payment.net_amount

    def _inverse_amount(self):
        """Update net_amount when total amount is set"""
        for payment in self:
            payment.net_amount = payment.amount - payment.paylines_amount

    @api.depends('checks_amount')
    def _compute_paylines_amount(self):
        """Compute paylines amount from checks"""
        for payment in self:
            payment.paylines_amount = payment.checks_amount