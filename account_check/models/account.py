# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AccountJournal(models.Model):
    """Extend account.journal to support check management functionality"""
    _inherit = 'account.journal'

    checkbook_ids = fields.One2many(
        comodel_name='account.checkbook',
        inverse_name='journal_id',
        string='Checkbooks',
        help="List of checkbooks associated with this journal"
    )
    under_collection_acc_id = fields.Many2one(
        comodel_name='account.account',
        string='Check Management Account',
        help="Account used for check management operations"
    )
    bank_under_collection_acc_id = fields.Many2one(
        comodel_name='account.account',
        string='Under Collection',
        help="Account for checks under collection"
    )
    handed_acc_id = fields.Many2one(
        comodel_name='account.account',
        string='Handed Checks Account',
        help="Account for handed checks"
    )
    long_term_account = fields.Many2one(
        comodel_name='account.account',
        string='Long Term Account',
        help="Account for long-term check operations"
    )
    payment_subtype = fields.Selection(
        selection='_get_payment_subtype',
        string='Payment Subtype',
        help="Type of payment (Issue Check or Third Check)"
    )

    @api.model
    def _get_payment_subtype(self):
        """Define available payment subtypes for check management"""
        return [
            ('issue_check', _('Issue Check')),
            ('third_check', _('Third Check')),
        ]