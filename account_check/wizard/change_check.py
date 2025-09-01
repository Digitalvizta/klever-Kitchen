# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class account_change_check(models.TransientModel):
    _name = 'account.change.check'
    _description = 'Account Change Check'


    @api.constrains('type', 'checkbook_id')
    def _check_checkbook_required(self):
        for rec in self:
            if rec.type == 'issue_check' and not rec.checkbook_id:
                raise ValidationError("You must select a Checkbook when type is 'issue_check'.")

    @api.model
    def get_original_check(self):
        return self.original_check_id.browse(self._context.get('active_id'))

    original_check_id = fields.Many2one(
        'account.check',
        'Original Check',
        required=True,
        default=get_original_check,
        ondelete='cascade',
        )
    journal_id = fields.Many2one(
        related='original_check_id.journal_id',
        )
    type = fields.Selection(
        related='original_check_id.type',
        )
    number = fields.Char(
        'Number',
        required=True,
        )
    issue_date = fields.Date(
        'Issue Date',
        required=True,
        default=fields.Date.context_today,
        )
    payment_date = fields.Date(
        'Payment Date',
        help="Only if this check is post dated",
        )

    # issue checks
    checkbook_id = fields.Many2one(
        'account.checkbook',
        'Checkbook mm',
        ondelete='cascade',
        )
    issue_check_subtype = fields.Selection(
        related='checkbook_id.issue_check_subtype',
        )

    # third checks
    bank_id = fields.Many2one(
        'res.bank', 'Bank',
        )
    vat = fields.Char(
        # TODO rename to Owner VAT
        'Owner Vat',
        )
    owner_name = fields.Char(
        'Owner Name',
        )

    @api.onchange('original_check_id')
    def change_original_check(self):
        self.checkbook_id = self.original_check_id.checkbook_id.id
        self.vat = self.original_check_id.vat
        self.owner_name = self.original_check_id.owner_name
        self.bank_id = self.original_check_id.bank_id.id


    def confirm(self):
        self.ensure_one()
        vals = {
            'vat': self.vat,
            'owner_name': self.owner_name,
            'checkbook_id': self.checkbook_id.id,
            'payment_date': self.payment_date,
            'issue_date': self.issue_date,
            'number': self.number,
        }
        new_check = self.original_check_id.copy(vals)
        self.original_check_id.write({
            'replacing_check_id': new_check.id,
            'amount': 0.0,
            'company_currency_amount': 0.0,
            })
        self.original_check_id.state = 'changed'
        if new_check.type == 'issue_check':
            new_check.state = 'handed'
        else:
            new_check.state = 'holding'
        return {
            'name': ('New Check'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.check',
            'view_id': self.env.ref('account_check.view_account_check_form').id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': new_check.id,
        }

