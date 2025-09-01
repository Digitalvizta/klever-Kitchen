# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from odoo.exceptions import UserError
from odoo import models, fields, api, _
from odoo.exceptions import  UserError, ValidationError


class account_check_action(models.TransientModel):
    _name = 'account.check.action'
    _description = 'Account Check'

    @api.model
    def _get_company_id(self):
        active_ids = self._context.get('active_ids', [])
        checks = self.env['account.check'].browse(active_ids)
        company_ids = [x.company_id.id for x in checks]
        if len(set(company_ids)) > 1:
            raise UserError(_('All checks must be from the same company!'))
        return self.env['res.company'].search(
            [('id', 'in', company_ids)], limit=1)

    @api.model
    def _get_companycheck(self):
        active_ids = self._context.get('active_ids', [])
        checks = self.env['account.check'].browse(active_ids)
        if checks:
            return checks[0].company_check
        else:
            return False

    journal_id = fields.Many2one(
        'account.journal',
        'Journal',
        domain="[('company_id','=',company_id), "
               "('type', 'in', ['cash', 'bank', 'general']), "
               "('payment_subtype', 'not in', ['issue_check', 'third_check'])]"
    )
    account_id = fields.Many2one(
        'account.account',
        'Account',

    )
    # account_id = fields.Many2one(
    #     'account.account',
    #     'Account',
    #     domain="[('company_id','=',company_id), "
    #            "('user_type_id', 'in', ('other', 'liquidity'))]"
    # )
    date = fields.Date(
        'Date', required=True, default=fields.Date.context_today
    )
    action_type = fields.Char(
        'Action type passed on the context', required=True
    )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        required=True,
        default=_get_company_id
    )

    debit_journal_id = fields.Many2one(
        'account.journal',
        'Journal',
        domain="[('company_id','=',company_id), "
               "('type', 'in', ['cash', 'bank', 'general']), "
               "('payment_subtype', 'not in', ['issue_check', 'third_check'])]"
    )
    companycheck = fields.Boolean(string="Company Check",default=_get_companycheck)

    # @api.onchange('journal_id')
    # def onchange_journal_id(self):
    #     self.account_id= self.journal_id.company_id.account_journal_payment_debit_account_id
        # sel f.account_id = self.journal_id.payment_debit_account_id.id

    @api.onchange('journal_id')
    def onchange_journal_id(self):
        if self.journal_id:
            account = (
                    getattr(self.journal_id, 'default_account_id', False) or
                    getattr(self.journal_id, 'default_debit_account_id', False) or
                    getattr(self.journal_id.company_id, 'account_journal_payment_debit_account_id', False)
            )
            self.account_id = account
        else:
            self.account_id = False

    @api.model
    def validate_action(self, action_type, check):
        # state controls
        if action_type == 'deposit':
            if check.type == 'third_check':
                if check.state != 'undercollection':
                    raise UserError(
                        _('The selected checks must be in Under Collection state.'))
            else:  # issue
                raise UserError(_('You can not deposit a Issue Check.'))
        elif action_type == 'debit':
            if check.type == 'issue_check':
                if check.state != 'handed':
                    raise UserError(
                        _('The selected checks must be in handed state.'))
            else:  # third
                raise UserError(_('You can not debit a Third Check.'))
        elif action_type == 'return':
            if check.type == 'third_check':
                if check.state != 'holding':
                    raise UserError(
                        _('The selected checks must be in holding state.'))
            # TODO implement return issue checs and return handed third checks
            else:  # issue
                raise UserError(_('You can not return a Issue Check.'))
        elif action_type == 'under_collection':
            if not self.journal_id.bank_under_collection_acc_id:
                raise UserError(_('The selected journal Does not have under collection account.'))
            if check.type == 'third_check':
                if check.state != 'holding':
                    raise UserError(
                        _('The selected checks must be in Holding state.'))
            else:  # third
                raise UserError(_('You can not depoist for under collection a Third Check.'))
        return True


    def action_confirm(self):
        self.ensure_one()

        # TODO used to get correct ir properties
        self = self.with_context(
            company_id=self.company_id.id,
            force_company=self.company_id.id,
        )

        for check in self.env['account.check'].browse(self._context.get('active_ids', [])):
            self.validate_action(self.action_type, check)
            vals = self.get_vals(self.action_type, check, self.date)

            aml_obj = self.env['account.move.line'].with_context(check_move_validity=False)
            currency=check.voucher_id.currency_id
            price_subtotal=check.amount

            if currency and currency !=  check.company_id.currency_id:

                balance = currency._convert(check.amount, check.company_id.currency_id, check.company_id, date=check.payment_date)
                amount_currency= price_subtotal
                debit= balance > 0.0 and balance or 0.0
                credit= balance < 0.0 and -balance or 0.0
                currency_id = currency.id

            else:
                amount_currency =  0.0
                debit =  price_subtotal > 0.0 and price_subtotal or 0.0
                credit =  price_subtotal < 0.0 and -price_subtotal or 0.0
                currency_id = check.company_id.currency_id.id  # Always provide currency_id
                # currency_id=False

            # extraemos los vals
            move_vals = vals.get('move_vals', {})
            debit_line_vals = vals.get('debit_line_vals', {})
            debit_line_vals.update({'debit': debit, 'credit': credit, 'amount_currency': amount_currency or False,
                                    'currency_id': currency_id})
            credit_line_vals = vals.get('credit_line_vals', {})
            credit_line_vals.update({'debit': credit, 'credit': debit, 'amount_currency': -1 * amount_currency or False,
                                     'currency_id': currency_id})
            check_move_field = vals.get('check_move_field')
            signal = vals.get('signal')
            move = self.env['account.move'].with_context({}).create(move_vals)
            debit_line_vals['move_id'] = move.id
            credit_line_vals['move_id'] = move.id
            # move.line_ids.with_context({}).create(debit_line_vals)
            aml_obj.create(debit_line_vals)
            # move.line_ids.with_context({}).create(credit_line_vals)
            aml_obj.create(credit_line_vals)
            check.write({check_move_field: move.id})

            check.state = signal
            move.action_post()
            # move.post()

        return True

    @api.model
    def get_vals(self, action_type, check, date):

        vou_journal = check.voucher_id.journal_id
        accounts = self.get_accounts(check)
        # TODO improove how we get vals, get them in other functions
        if self.action_type == 'deposit':
            ref = _('Deposit Check Nr. ')
            check_move_field = 'deposit_account_move_id'
            journal = self.journal_id
            debit_account_id = accounts['debit_account_id']
            partner = check.source_partner_id.id,
            credit_account_id = accounts['credit_account_id']
            signal = 'deposited'
        elif self.action_type == 'debit':
            ref = _('Debit Check Nr. ')
            check_move_field = 'debit_account_move_id'
            journal = check.checkbook_id.debit_journal_id
            partner = check.destiny_partner_id.id
            debit_account_id = accounts['debit_account_id']
            credit_account_id = accounts['credit_account_id']
            signal = 'debited'
        elif self.action_type == 'return':
            ref = _('Return Check Nr. ')
            check_move_field = 'return_account_move_id'
            journal = vou_journal
            debit_account_id = accounts['debit_account_id']
            partner = check.source_partner_id.id,
            credit_account_id = accounts['credit_account_id']
            signal = 'returned'
        elif self.action_type == 'under_collection':
            ref = _('Under Collection Check Nr. ')
            check_move_field =  'under_collect_move_id'
            journal = self.journal_id
            debit_account_id = accounts['debit_account_id']
            partner = check.source_partner_id.id,
            credit_account_id = accounts['credit_account_id']
            signal = 'undercollection'

            # TODO Update invoice residual when check returned
            payment_id = check.voucher_id
            invoice_ids = payment_id.reconciled_invoice_ids
            self.env['return.invoice_residual'].return_invoice_residual(invoice_ids=invoice_ids)



        ref += check.name

        move_vals = {
            'journal_id': journal.id,
            'date': self.date,
            'ref': ref,
            'company_id': check.company_id.id
        }

        debit_line_vals = {
            'account_id': debit_account_id,
            'partner_id': partner,
            'debit': check.company_currency_amount or check.amount,
            'amount_currency': (
                    check.company_currency_amount and check.amount or False),
            'ref': ref,
        }
        credit_line_vals = {
            'account_id': credit_account_id,
            'partner_id': partner,
            'credit': check.company_currency_amount or check.amount,
            'amount_currency': (
                    check.company_currency_amount and (
                    -1 * check.amount) or False),
            'ref': ref,
        }
        return {
            'move_vals': move_vals,
            'debit_line_vals': debit_line_vals,
            'credit_line_vals': credit_line_vals,
            'check_move_field': check_move_field,
            'signal': signal,
        }

    def get_accounts(self,check):
        vals = {}
        if self.action_type == 'under_collection':
            if check.long_term_check:
                vals['credit_account_id'] = check.voucher_id.journal_id.long_term_account.id
            else:
                vals['credit_account_id'] = check.voucher_id.journal_id.under_collection_acc_id.id
            vals['debit_account_id'] = self.journal_id.bank_under_collection_acc_id.id
            check.under_collection_account_id = vals['debit_account_id']
        if self.action_type == 'deposit':
            vals['credit_account_id'] = check.under_collection_account_id.id
            # vals['debit_account_id'] = self.journal_id.company_id.account_journal_payment_debit_account_id.id
            vals['debit_account_id'] = check.source_partner_id.property_account_receivable_id.id
        if self.action_type == 'return':
            vals['credit_account_id'] = check.voucher_id.journal_id.under_collection_acc_id.id
            vals['debit_account_id'] =  check.source_partner_id.property_account_receivable_id.id
        if self.action_type == 'debit':
            if check.long_term_check:
                vals['debit_account_id'] = check.voucher_id.journal_id.long_term_account.id
            else:
                vals['debit_account_id'] = check.voucher_id.journal_id.handed_acc_id.id
            vals['credit_account_id'] = check.voucher_id.journal_id.company_id.account_journal_payment_credit_account_id.id
        return vals

