# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from odoo.exceptions import UserError
from odoo import models, fields, api, _
from datetime import date, datetime


class account_check_dreject(models.TransientModel):
    _name = 'account.check.dreject'
    _description = 'Check Reject'

    @api.model
    def _get_company_id(self):
        active_ids = self._context.get('active_ids', [])
        checks = self.env['account.check'].browse(active_ids)
        company_ids = [x.company_id.id for x in checks]
        if len(set(company_ids)) > 1:
            raise UserError(_('All checks must be from the same company!'))
        return self.env['res.company'].search(
            [('id', 'in', company_ids)], limit=1)

    type = fields.Char(
        'Check Type')
    state = fields.Char(
        'Check State')
    reject_date = fields.Date(
        'Reject Date', required=True, default=fields.Date.context_today)
    expense_account = fields.Many2one(
        'account.account',
        'Expense Account',

    )
    # domain = [('type', 'in', ['other'])],
    has_expense = fields.Boolean(
        'Has Expense', default=True)
    expense_amount = fields.Float(
        'Expense Amount')
    expense_to_customer = fields.Boolean(
        'Expenses to Customer')
    company_id = fields.Many2one(
        'res.company',
        'Company',
        required=True,
        default=_get_company_id)


    # def action_dreject(self):
    #     self.ensure_one()
    #
    #     # used to get correct ir properties
    #     self = self.with_context(
    #         company_id=self.company_id.id,
    #         force_company=self.company_id.id,
    #     )
    #
    #
    #     # TODO Handel Checks Rejection
    #     for check in self.env['account.check'].browse(
    #             self._context.get('active_ids', [])):
    #         if check.state not in ['undercollection', 'handed']:
    #             raise UserError(
    #                 _('Only Under Collection or handed checks can be rejected.'))
    #
    #
    #         ref = _('Check Rejected N: ')
    #         ref += check.name
    #
    #         move = {
    #
    #             'journal_id': check.voucher_id.journal_id.id,
    #             'date': self.reject_date,
    #             'ref': _('Rejected Check Nr. ') + check.name,
    #             'partner_id': check.destiny_partner_id.id or check.source_partner_id.id,
    #         }
    #
    #         move_lines = {
    #
    #             'partner_id': check.destiny_partner_id.id or check.source_partner_id.id,
    #             # 'centralisation': 'normal',
    #         }
    #         credit = []
    #         debit = []
    #
    #         if check.type == 'third_check':
    #             if self.has_expense and self.expense_to_customer:
    #                 credit.append({
    #                     'account': check.under_collect_move_id.journal_id.bank_under_collection_acc_id.id,
    #                     'amount': check.amount,
    #                 })
    #                 credit.append({
    #                     'account': self.expense_account.id,
    #                     'amount': self.expense_amount,
    #                 })
    #                 debit.append({
    #                     'account': check.voucher_id.partner_id.property_account_receivable_id.id,
    #                     'amount': (check.amount + self.expense_amount),
    #                 })
    #             elif self.has_expense:
    #                 # self.make_expenses_move(check)
    #                 debit.append({
    #                     'account': check.voucher_id.partner_id.property_account_receivable_id.id,
    #                     'amount': check.amount,
    #                 })
    #                 debit.append({
    #                     'account': self.expense_account.id,
    #                     'amount': self.expense_amount,
    #                 })
    #                 credit.append({
    #                     'account': check.under_collect_move_id.journal_id.bank_under_collection_acc_id.id,
    #                     'amount': (check.amount + self.expense_amount),
    #                 })
    #             elif not self.has_expense:
    #                 debit.append({
    #                     'account': check.voucher_id.partner_id.property_account_receivable_id.id,
    #                     'amount': check.amount,
    #                 })
    #                 credit.append({
    #                     'account': check.under_collect_move_id.journal_id.bank_under_collection_acc_id.id,
    #                     'amount': check.amount,
    #                 })
    #
    #             self.create_moves(move=move,
    #                               move_line=move_lines,
    #                               debit_account=debit,
    #                               credit_account=credit,
    #                               src_currency=self.company_id.currency_id,
    #                               amount=0)
    #
    #             payment_id = check.voucher_id
    #             invoice_ids = payment_id.reconciled_invoice_ids
    #             self.env['return.invoice_residual'].return_invoice_residual(invoice_ids=invoice_ids)
    #
    #         if check.state == 'handed':
    #             if self.has_expense:
    #                 if check.long_term_check:
    #                     debit.append({
    #                         'account': check.voucher_id.journal_id.long_term_account.id,
    #                         'amount': check.amount,
    #                     })
    #                 else:
    #                     debit.append({
    #                         'account': check.voucher_id.journal_id.handed_acc_id.id,
    #                         'amount': check.amount,
    #                     })
    #                 debit.append({
    #                     'account': self.expense_account.id,
    #                     'amount': self.expense_amount,
    #                 })
    #                 credit.append({
    #                     'account': check.voucher_id.partner_id.property_account_payable_id.id,
    #                     'amount': (check.amount + self.expense_amount),
    #                 })
    #
    #             else:
    #                 if check.long_term_check:
    #                     debit.append({
    #                         'account': check.voucher_id.journal_id.long_term_account.id,
    #                         'amount': check.amount,
    #                     })
    #                 else:
    #                     debit.append({
    #                         'account': check.voucher_id.journal_id.handed_acc_id.id,
    #                         'amount': check.amount,
    #                     })
    #                 credit.append({
    #                     'account': check.voucher_id.partner_id.property_account_payable_id.id,
    #                     'amount': check.amount,
    #                 })
    #
    #             self.create_moves(move=move,
    #                               move_line=move_lines,
    #                               debit_account=debit,
    #                               credit_account=credit,
    #                               src_currency=self.company_id.currency_id,
    #                               amount=0)
    #             payment_id = check.voucher_id
    #             invoice_ids = payment_id.reconciled_invoice_ids
    #             self.env['return.invoice_residual'].return_invoice_residual(invoice_ids=invoice_ids)
    #         check.state = 'rejected'

    def action_dreject(self, *args, **kwargs):
        self.ensure_one()

        # Set context for company-specific properties
        self = self.with_context(
            company_id=self.company_id.id,
            force_company=self.company_id.id,
        )

        # Process each check
        for check in self.env['account.check'].browse(self._context.get('active_ids', [])):
            if check.state not in ['undercollection', 'handed']:
                raise UserError(_('Only Under Collection or handed checks can be rejected.'))

            ref = _('Check Rejected N: ') + check.name

            # Define base move data with currency_id
            move = {
                'journal_id': check.voucher_id.journal_id.id,
                'date': self.reject_date,
                'ref': _('Rejected Check Nr. ') + check.name,
                'partner_id': check.destiny_partner_id.id or check.source_partner_id.id,
                'company_id': self.company_id.id,
                'currency_id': self.company_id.currency_id.id,  # Ensure currency_id for move
            }

            move_lines = {
                'partner_id': check.destiny_partner_id.id or check.source_partner_id.id,
                'currency_id': self.company_id.currency_id.id,  # Ensure currency_id for lines
            }

            credit = []
            debit = []
            currency_id = self.company_id.currency_id.id  # Get currency ID

            if check.type == 'third_check':
                if self.has_expense and self.expense_to_customer:
                    credit.append({
                        'account': check.under_collect_move_id.journal_id.bank_under_collection_acc_id.id,
                        'amount': check.amount,
                        'currency_id': currency_id,
                        'partner_id': check.destiny_partner_id.id or check.source_partner_id.id,
                    })
                    credit.append({
                        'account': self.expense_account.id,
                        'amount': self.expense_amount,
                        'currency_id': currency_id,
                        'partner_id': check.destiny_partner_id.id or check.source_partner_id.id,
                    })
                    debit.append({
                        'account': check.voucher_id.partner_id.property_account_receivable_id.id,
                        'amount': check.amount + self.expense_amount,
                        'currency_id': currency_id,
                        'partner_id': check.destiny_partner_id.id or check.source_partner_id.id,
                    })
                elif self.has_expense:
                    debit.append({
                        'account': check.voucher_id.partner_id.property_account_receivable_id.id,
                        'amount': check.amount,
                        'currency_id': currency_id,
                        'partner_id': check.destiny_partner_id.id or check.source_partner_id.id,
                    })
                    debit.append({
                        'account': self.expense_account.id,
                        'amount': self.expense_amount,
                        'currency_id': currency_id,
                        'partner_id': check.destiny_partner_id.id or check.source_partner_id.id,
                    })
                    credit.append({
                        'account': check.under_collect_move_id.journal_id.bank_under_collection_acc_id.id,
                        'amount': check.amount + self.expense_amount,
                        'currency_id': currency_id,
                        'partner_id': check.destiny_partner_id.id or check.source_partner_id.id,
                    })
                else:
                    debit.append({
                        'account': check.voucher_id.partner_id.property_account_receivable_id.id,
                        'amount': check.amount,
                        'currency_id': currency_id,
                        'partner_id': check.destiny_partner_id.id or check.source_partner_id.id,
                    })
                    credit.append({
                        'account': check.under_collect_move_id.journal_id.bank_under_collection_acc_id.id,
                        'amount': check.amount,
                        'currency_id': currency_id,
                        'partner_id': check.destiny_partner_id.id or check.source_partner_id.id,
                    })

                self.create_moves(
                    move=move,
                    move_line=move_lines,
                    debit_account=debit,
                    credit_account=credit,
                    src_currency=self.company_id.currency_id,
                    amount=0
                )

                payment_id = check.voucher_id
                invoice_ids = payment_id.reconciled_invoice_ids
                self.env['return.invoice_residual'].return_invoice_residual(invoice_ids=invoice_ids)

            if check.state == 'handed':
                if self.has_expense:
                    debit.append({
                        'account': check.voucher_id.journal_id.long_term_account.id if check.long_term_check else check.voucher_id.journal_id.handed_acc_id.id,
                        'amount': check.amount,
                        'currency_id': currency_id,
                        'partner_id': check.destiny_partner_id.id or check.source_partner_id.id,
                    })
                    debit.append({
                        'account': self.expense_account.id,
                        'amount': self.expense_amount,
                        'currency_id': currency_id,
                        'partner_id': check.destiny_partner_id.id or check.source_partner_id.id,
                    })
                    credit.append({
                        'account': check.voucher_id.partner_id.property_account_payable_id.id,
                        'amount': check.amount + self.expense_amount,
                        'currency_id': currency_id,
                        'partner_id': check.destiny_partner_id.id or check.source_partner_id.id,
                    })
                else:
                    debit.append({
                        'account': check.voucher_id.journal_id.long_term_account.id if check.long_term_check else check.voucher_id.journal_id.handed_acc_id.id,
                        'amount': check.amount,
                        'currency_id': currency_id,
                        'partner_id': check.destiny_partner_id.id or check.source_partner_id.id,
                    })
                    credit.append({
                        'account': check.voucher_id.partner_id.property_account_payable_id.id,
                        'amount': check.amount,
                        'currency_id': currency_id,
                        'partner_id': check.destiny_partner_id.id or check.source_partner_id.id,
                    })

                self.create_moves(
                    move=move,
                    move_line=move_lines,
                    debit_account=debit,
                    credit_account=credit,
                    src_currency=self.company_id.currency_id,
                    amount=0
                )

                payment_id = check.voucher_id
                invoice_ids = payment_id.reconciled_invoice_ids
                self.env['return.invoice_residual'].return_invoice_residual(invoice_ids=invoice_ids)

            check.state = 'rejected'

        return {'type': 'ir.actions.act_window_close'}

    def create_moves(self, move, move_line, debit_account, credit_account, src_currency, amount):
        move_vals = move.copy()
        move_vals['line_ids'] = []
        for line in debit_account:
            move_vals['line_ids'].append((0, 0, {
                'account_id': line['account'],
                'debit': line['amount'],
                'partner_id': move_line.get('partner_id'),
                'currency_id': line.get('currency_id', src_currency.id),  # Add currency_id
            }))
        for line in credit_account:
            move_vals['line_ids'].append((0, 0, {
                'account_id': line['account'],
                'credit': line['amount'],
                'partner_id': move_line.get('partner_id'),
                'currency_id': line.get('currency_id', src_currency.id),  # Add currency_id
            }))
        self.env['account.move'].create(move_vals)

    # def create_moves(self, **kwargs):
    #     aml_obj = self.env['account.move.line'].with_context(check_move_validity=False)
    #     company = self.env['res.users'].browse([self._uid]).company_id
    #     company_currency = company.currency_id
    #
    #     currency = kwargs['src_currency']
    #     price_subtotal = kwargs['amount']
    #
    #     if currency and currency != company_currency:
    #
    #         balance = currency._convert(kwargs['amount'], company_currency, company,date=datetime.today())
    #         amount_currency = price_subtotal
    #         debit = balance > 0.0 and balance or 0.0
    #         credit = balance < 0.0 and -balance or 0.0
    #         currency_id = currency.id
    #
    #     else:
    #         amount_currency = 0.0
    #         debit = price_subtotal > 0.0 and price_subtotal or 0.0
    #         credit = price_subtotal < 0.0 and -price_subtotal or 0.0
    #         currency_id = False
    #
    #
    #
    #
    #     move = self.with_context({}).env['account.move'].create(kwargs['move'])
    #     for line in kwargs['credit_account']:
    #         move_line = kwargs['move_line']
    #         move_line.update({
    #             'move_id': move.id,
    #             'account_id': line['account'],
    #             'debit': debit,
    #             'credit': line['amount'],
    #             'amount_currency': amount_currency,
    #             'currency_id': currency_id,
    #         })
    #         aml_obj.create(move_line)
    #
    #     for line in kwargs['debit_account']:
    #         move_line = kwargs['move_line']
    #         move_line.update({
    #             'move_id': move.id,
    #             'account_id': line['account'],
    #             'debit': line['amount'],
    #             'credit': credit,
    #             'amount_currency': amount_currency,
    #             'currency_id': currency_id,
    #         })
    #         aml_obj.create(move_line)
    #     move.post()
    #     return True



# TODO return invoice residual when check returned
class ReturnInvoiceResidual(models.Model):
    _name = 'return.invoice_residual'
    _description = 'Return Invoice Residual'

    @api.model
    def return_invoice_residual(self, invoice_ids):
        if invoice_ids:
            for invoice in invoice_ids:
                for line in invoice.sudo().line_ids:
                    line.remove_move_reconcile()

