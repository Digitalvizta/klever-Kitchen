# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class AccountCheck(models.Model):
    """Manage checks (issued or third-party) for payments"""
    _name = 'account.check'
    _description = 'Account Check'
    _order = "id desc"
    _inherit = ['mail.thread']

    name = fields.Char(
        compute='_compute_name',
        string='Number',
        store=True,
        help="Formatted check number with padding"
    )
    number = fields.Char(
        string='Number',
        required=True,
        copy=False,
        help="Raw check number"
    )
    amount = fields.Monetary(
        string='Amount',
        required=True,
        digits='Account',
        help="Check amount in the payment currency"
    )
    company_currency_amount = fields.Monetary(
        string='Company Currency Amount',
        digits='Account',
        help="Check amount in company currency if different from payment currency"
    )
    voucher_id = fields.Many2one(
        comodel_name='account.payment',
        string='Payment',
        required=True,
        ondelete='cascade',
        help="Associated payment record"
    )
    type = fields.Selection(
        related='voucher_id.journal_id.payment_subtype',
        string='Type',
        store=True,
        help="Check type (Issue Check or Third Check)"
    )
    journal_id = fields.Many2one(
        comodel_name='account.journal',
        related='voucher_id.journal_id',
        string='Journal',
        store=True,
        help="Journal from the associated payment"
    )
    issue_date = fields.Date(
        string='Issue Date',
        required=True,
        default=fields.Date.context_today,
        help="Date the check was issued"
    )
    payment_date = fields.Date(
        string='Payment Date',
        help="Payment date for post-dated checks"
    )
    destiny_partner_id = fields.Many2one(
        comodel_name='res.partner',
        compute='_compute_destiny_partner',
        string='Destiny Partner',
        store=True,
        help="Partner receiving the check"
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User',
        default=lambda self: self.env.user,
        help="User who created the check"
    )
    clearing = fields.Selection(
        [('24', '24 hs'), ('48', '48 hs'), ('72', '72 hs')],
        string='Clearing',
        help="Check clearing period"
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('holding', 'Holding'),
            ('undercollection', 'Under Collection'),
            ('deposited', 'Deposited'),
            ('handed', 'Handed'),
            ('rejected', 'Rejected'),
            ('debited', 'Debited'),
            ('returned', 'Returned'),
            ('changed', 'Changed'),
            ('cancel', 'Cancel'),
        ],
        string='State',
        required=True,
        tracking=True,
        default='draft',
        copy=False,
        help="Current state of the check"
    )
    supplier_reject_debit_note_id = fields.Many2one(
        comodel_name='account.move',
        string='Supplier Reject Debit Note',
        copy=False,
        help="Debit note for supplier rejection"
    )
    expense_account_move_id = fields.Many2one(
        comodel_name='account.move',
        string='Expense Account Move',
        copy=False,
        help="Account move for expenses"
    )
    replacing_check_id = fields.Many2one(
        comodel_name='account.check',
        string='Replacing Check',
        copy=False,
        help="Check that replaces this one"
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        related='voucher_id.company_id',
        string='Company',
        store=True,
        help="Company associated with the payment"
    )
    issue_check_subtype = fields.Selection(
        related='checkbook_id.issue_check_subtype',
        string='Subtype',
        store=True,
        help="Subtype of issued check (Deferred or Currents)"
    )
    checkbook_id = fields.Many2one(
        comodel_name='account.checkbook',
        string='Checkbook',
        default=lambda self: self._get_checkbook(),
        help="Checkbook for issued checks",
    )
    debit_account_move_id = fields.Many2one(
        comodel_name='account.move',
        string='Debit Account Move',
        copy=False,
        help="Account move for debit"
    )
    third_handed_voucher_id = fields.Many2one(
        comodel_name='account.payment',
        string='Handed Payment',
        store=True,
        help="Payment where third check was handed"
    )
    source_partner_id = fields.Many2one(
        comodel_name='res.partner',
        compute='_compute_source_partner',
        string='Source Partner',
        store=True,
        help="Partner who provided the third check"
    )
    customer_reject_debit_note_id = fields.Many2one(
        comodel_name='account.move',
        string='Customer Reject Debit Note',
        copy=False,
        help="Debit note for customer rejection"
    )
    bank_id = fields.Many2one(
        comodel_name='res.bank',
        string='Bank',
        help="Bank issuing the check"
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        related='voucher_id.currency_id',
        help="Currency of the payment"
    )
    vat = fields.Char(
        string='Owner VAT',
        help="VAT of the check owner"
    )
    owner_name = fields.Char(
        string='Owner Name',
        help="Name of the check owner"
    )
    deposit_account_move_id = fields.Many2one(
        comodel_name='account.move',
        string='Deposit Account Move',
        copy=False,
        help="Account move for deposit"
    )
    return_account_move_id = fields.Many2one(
        comodel_name='account.move',
        string='Return Account Move',
        copy=False,
        help="Account move for return"
    )
    under_collect_move_id = fields.Many2one(
        comodel_name='account.move',
        string='Under Collect Account Move',
        copy=False,
        help="Account move for under collection"
    )
    long_term_check = fields.Boolean(
        string='Long Term Check',
        help="Indicates if the check is long-term"
    )
    company_check = fields.Boolean(
        string='Company Check',
        help="Indicates if the check is issued by the company"
    )
    under_collection_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Under Collection Account',
        help="Account for checks under collection"
    )

    @api.model
    def _get_checkbook(self):
        """Get default checkbook for issued checks"""
        journal_id = self._context.get('default_journal_id', False)
        payment_subtype = self._context.get('default_type', False)
        if journal_id and payment_subtype == 'issue_check':
            checkbooks = self.env['account.checkbook'].search(
                [('state', '=', 'active'), ('journal_id', '=', journal_id)], limit=1
            )
            return checkbooks or False
        return False

    @api.depends('number', 'checkbook_id', 'checkbook_id.padding')
    def _compute_name(self):
        """Compute formatted check number with padding"""
        for check in self:
            padding = check.checkbook_id.padding if check.checkbook_id else 8
            if check.type == 'issue_check' and check.checkbook_id:
                prefix = check.checkbook_id.number_prefix or ''
                check.name = f"{prefix}{check.number.zfill(padding)}"
            else:
                check.name = check.number.zfill(padding) if check.number else f"%0{padding}d" % 0

    @api.depends('voucher_id', 'voucher_id.partner_id', 'type', 'third_handed_voucher_id', 'third_handed_voucher_id.partner_id')
    def _compute_destiny_partner(self):
        """Compute the partner receiving the check"""
        for check in self:
            partner_id = (
                check.third_handed_voucher_id.partner_id.id
                if check.type == 'third_check' and check.third_handed_voucher_id
                else check.voucher_id.partner_id.id
                if check.type == 'issue_check'
                else False
            )
            check.destiny_partner_id = partner_id

    @api.depends('voucher_id', 'voucher_id.partner_id', 'type')
    def _compute_source_partner(self):
        """Compute the partner who provided the third check"""
        for check in self:
            check.source_partner_id = check.voucher_id.partner_id.id if check.type == 'third_check' else False

    @api.constrains('number', 'checkbook_id', 'type')
    def _check_number_issue(self):
        """Ensure check number is unique per checkbook for issued checks"""
        for check in self:
            if check.type == 'issue_check' and check.checkbook_id:
                duplicates = self.search([
                    ('id', '!=', check.id),
                    ('number', '=', check.number),
                    ('checkbook_id', '=', check.checkbook_id.id)
                ])
                if duplicates:
                    raise UserError(_('Check Number must be unique per Checkbook'))

    @api.constrains('number', 'bank_id')
    def _check_number_third(self):
        """Ensure third check number is unique per owner and bank"""
        for check in self:
            if check.type == 'third_check':
                duplicates = self.search([
                    ('id', '!=', check.id),
                    ('number', '=', check.number),
                    ('voucher_id.partner_id', '=', check.voucher_id.partner_id.id)
                ])
                if duplicates:
                    raise UserError(_('Check Number must be unique per Owner and Bank'))

    @api.onchange('issue_date', 'payment_date')
    def _onchange_date(self):
        """Validate payment date is after issue date"""
        if self.issue_date and self.payment_date and self.issue_date > self.payment_date:
            self.payment_date = False
            raise UserError(_('Payment Date must be greater than Issue Date'))

    @api.onchange('voucher_id')
    def _onchange_voucher(self):
        """Set owner details from payment partner"""
        if self.voucher_id:
            self.owner_name = self.voucher_id.partner_id.name
            self.vat = self.voucher_id.partner_id.vat

    @api.onchange('checkbook_id')
    def _onchange_checkbook(self):
        """Set check number from checkbook"""
        if self.checkbook_id:
            self.number = str(self.checkbook_id.next_check_number)

    def unlink(self):
        """Allow deletion only in draft state"""
        if any(check.state != 'draft' for check in self):
            raise UserError(_('Checks can only be deleted in Draft state'))
        return super().unlink()

    def action_cancel_draft(self):
        """Reset check to draft state"""
        self.write({'state': 'draft'})
        return True

    def action_hold(self):
        """Set check state to holding"""
        self.write({'state': 'holding'})
        return True

    def action_deposit(self):
        """Set check state to deposited"""
        self.write({'state': 'deposited'})
        return True

    def action_return(self):
        """Set check state to returned"""
        self.write({'state': 'returned'})
        return True

    def action_change(self):
        """Set check state to changed"""
        self.write({'state': 'changed'})
        return True

    def action_hand(self):
        """Set check state to handed"""
        self.write({'state': 'handed'})
        return True

    def action_reject(self):
        """Set check state to rejected"""
        self.write({'state': 'rejected'})
        return True

    def action_debit(self):
        """Set check state to debited"""
        self.write({'state': 'debited'})
        return True

    def action_cancel_rejection(self):
        """Cancel rejection and revert to appropriate state"""
        for check in self:
            if check.customer_reject_debit_note_id or check.supplier_reject_debit_note_id or check.expense_account_move_id:
                raise UserError(_('Cannot cancel rejection: Delete related debit notes or expense moves first'))
            check.state = 'handed' if check.type == 'issue_check' else 'holding'
        return True

    def action_cancel_debit(self):
        """Cancel debit and revert to handed state for issued checks"""
        for check in self:
            if check.debit_account_move_id:
                raise UserError(_('Cannot cancel debit: Delete Debit Account Move first'))
            if check.type == 'issue_check':
                check.action_hand()
        return True

    def action_cancel_deposit(self):
        """Cancel deposit and revert to holding state"""
        for check in self:
            if check.deposit_account_move_id:
                raise UserError(_('Cannot cancel deposit: Delete Deposit Account Move first'))
            check.action_hold()
        return True

    def action_cancel_return(self):
        """Cancel return and revert to holding state"""
        for check in self:
            if check.return_account_move_id:
                raise UserError(_('Cannot cancel return: Delete Return Account Move first'))
            check.action_hold()
        return True

    def check_check_cancellation(self):
        """Validate check cancellation conditions"""
        for check in self:
            if check.type == 'issue_check' and check.state not in ['draft', 'handed']:
                raise UserError(_('Issued checks can only be canceled in Draft or Handed state'))
            elif check.type == 'third_check' and check.state not in ['draft', 'holding']:
                raise UserError(_('Third checks can only be canceled in Draft or Holding state'))
            elif check.type == 'third_check' and check.third_handed_voucher_id:
                raise UserError(_('Cannot cancel third checks used in payments'))
        return True

    def action_cancel(self):
        """Set check state to cancel"""
        self.check_check_cancellation()
        self.write({'state': 'cancel'})
        return True

    def _adjust_longterm_checks(self):
        """Adjust long-term checks to normal accounts when due"""
        _logger.debug("Running _adjust_longterm_checks")
        for check in self.search([('long_term_check', '=', True)]):
            current_year_end = fields.Date.today().replace(month=12, day=31)
            check_date = fields.Date.from_string(check.issue_date)
            if check_date <= current_year_end and check.state in ('holding', 'handed'):
                _logger.debug("Handling check %s", check.number)
                # Ensure journal and accounts are valid
                if not check.voucher_id.journal_id or not check.voucher_id.company_id:
                    _logger.error("Invalid journal or company for check %s", check.number)
                    continue
                if not check.voucher_id.journal_id.long_term_account or not check.voucher_id.journal_id.under_collection_acc_id:
                    _logger.error("Missing required accounts for check %s", check.number)
                    continue
                # Create move in draft state
                move_vals = self.get_move_vals(check)
                move = self.env['account.move'].with_context(check_move_validity=False).create(move_vals)
                # Create move lines
                debit_line_vals = self.get_move_debit_line(check)
                credit_line_vals = self.get_move_credit_line(check)
                debit_line_vals['move_id'] = move.id
                credit_line_vals['move_id'] = move.id
                self.env['account.move.line'].with_context(check_move_validity=False).create([debit_line_vals, credit_line_vals])
                # Post the move
                try:
                    move.action_post()
                    check.long_term_check = False
                    check.under_collect_move_id = move
                except Exception as e:
                    _logger.error("Failed to post move for check %s: %s", check.number, str(e))
                    raise UserError(_('Failed to adjust long-term check %s: %s') % (check.number, str(e)))

    def get_move_vals(self, check):
        """Prepare values for account move for long-term check adjustment"""
        return {
            'journal_id': check.voucher_id.journal_id.id,
            'date': fields.Date.today(),
            'ref': 'Change check account from long term to normal account for check %s' % check.number,
            'company_id': check.company_id.id,
            'move_type': 'entry',  # Explicitly set move type to avoid conflicts
        }

    def get_move_debit_line(self, check):
        """Prepare debit line for long-term check adjustment"""
        amount = check.company_currency_amount or check.amount
        debit_account = (
            check.voucher_id.journal_id.under_collection_acc_id
            if check.state == 'holding'
            else check.voucher_id.journal_id.long_term_account
        )
        if not debit_account:
            raise UserError(_('No debit account configured for check %s') % check.number)
        return {
            'account_id': debit_account.id,
            'partner_id': check.voucher_id.partner_id.id if check.voucher_id.partner_id else False,
            'debit': amount,
            'amount_currency': amount if check.company_currency_amount else False,
            'currency_id': check.currency_id.id if check.company_currency_amount else False,
            'ref': 'Change check account for check %s' % check.number,
        }

    def get_move_credit_line(self, check):
        """Prepare credit line for long-term check adjustment"""
        amount = check.company_currency_amount or check.amount
        credit_account = (
            check.voucher_id.journal_id.long_term_account
            if check.state == 'holding'
            else check.voucher_id.journal_id.handed_acc_id
        )
        if not credit_account:
            raise UserError(_('No credit account configured for check %s') % check.number)
        return {
            'account_id': credit_account.id,
            'partner_id': check.voucher_id.partner_id.id if check.voucher_id.partner_id else False,
            'credit': amount,
            'amount_currency': -amount if check.company_currency_amount else False,
            'currency_id': check.currency_id.id if check.company_currency_amount else False,
            'ref': 'Change check account for check %s' % check.number,
        }

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        """Customize state selection based on check type"""
        res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if 'fields' in res and 'state' in res['fields'] and 'selection' in res['fields']['state']:
            third_checks = self.env.context.get('menu_third_checks')
            issue_checks = self.env.context.get('menu_issue_checks')
            state_selection = res['fields']['state']['selection'][:]
            if third_checks:
                state_selection = [s for s in state_selection if s[0] not in ['handed', 'debited', 'cancel']]
            elif issue_checks:
                state_selection = [s for s in state_selection if s[0] not in ['holding', 'undercollection', 'deposited', 'cancel', 'returned']]
            res['fields']['state']['selection'] = state_selection
        return res