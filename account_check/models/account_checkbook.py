# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class AccountCheckbook(models.Model):
    """Manage checkbooks for bank journals"""
    _name = 'account.checkbook'
    _description = 'Account Checkbook'
    _inherit = ['mail.thread']
    _order = "name"

    name = fields.Char(
        string='Name',
        required=True,
        help="Unique identifier for the checkbook"
    )
    issue_check_subtype = fields.Selection(
        [('deferred', 'Deferred'), ('currents', 'Currents')],
        string='Issue Check Subtype',
        required=True,
        default='deferred',
        help="Deferred checks require a payment date; currents do not"
    )
    number_prefix = fields.Char(
        string="Check Book Numbering Prefix",
        help="Prefix for check numbers"
    )
    debit_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Debit Journal',
        required=True,
        domain=[('type', '=', 'bank')],
        context={'default_type': 'bank'},
        help="Journal used for debiting checks"
    )
    journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Journal',
        required=True,
        domain=[('type', '=', 'bank')],
        context={'default_type': 'bank'},
        help="Journal where the checkbook is used"
    )
    range_from = fields.Integer(
        string='From Check Number',
        required=True,
        help="Starting check number in the range"
    )
    range_to = fields.Integer(
        string='To Check Number',
        required=True,
        help="Ending check number in the range"
    )
    next_check_number = fields.Integer(
        compute='_compute_next_check_number',
        string='Next Check Number',
        help="Next available check number"
    )
    padding = fields.Integer(
        string='Number Padding',
        default=8,
        required=True,
        help="Number of zeros to pad check numbers"
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        related='journal_id.company_id',
        string='Company',
        store=True,
        help="Company associated with the journal"
    )
    issue_check_ids = fields.One2many(
        comodel_name='account.check',
        inverse_name='checkbook_id',
        string='Issue Checks',
        help="Checks issued from this checkbook"
    )
    state = fields.Selection(
        [('draft', 'Draft'), ('active', 'In Use'), ('used', 'Used')],
        string='State',
        default='draft',
        copy=False,
        help="Current state of the checkbook"
    )

    @api.depends('issue_check_ids.number', 'range_from')
    def _compute_next_check_number(self):
        """Compute the next available check number"""
        for checkbook in self:
            check_numbers = [
                int(check.number) for check in checkbook.issue_check_ids
                if check.number and check.number.isdigit()
            ]
            checkbook.next_check_number = max(check_numbers + [checkbook.range_from]) + 1 if check_numbers else checkbook.range_from

    @api.constrains('range_to', 'range_from')
    def _check_numbers(self):
        """Ensure range_to is greater than range_from"""
        for checkbook in self:
            if checkbook.range_to <= checkbook.range_from:
                raise UserError(_('Range To must be greater than Range From'))

    @api.constrains('padding')
    @api.onchange('padding')
    def _check_padding(self):
        """Validate padding is less than 32"""
        for checkbook in self:
            if checkbook.padding > 32:
                raise UserError(_('Padding must be less than 32'))

    @api.constrains('debit_journal_id', 'journal_id')
    def _check_journals(self):
        """Ensure journal and debit journal belong to the same company"""
        for checkbook in self:
            if checkbook.journal_id.company_id != checkbook.debit_journal_id.company_id:
                raise UserError(_('Journal and Debit Journal must belong to the same company'))

    def unlink(self):
        """Allow deletion only in draft state"""
        if any(checkbook.state != 'draft' for checkbook in self):
            raise UserError(_('You can only delete checkbooks in Draft state'))
        return super().unlink()

    def set_used(self):
        """Mark checkbook as used"""
        self.write({'state': 'used'})
        return True

    def set_active(self):
        """Mark checkbook as active"""
        self.write({'state': 'active'})
        return True

    def set_draft(self):
        """Mark checkbook as draft"""
        self.write({'state': 'draft'})
        return True