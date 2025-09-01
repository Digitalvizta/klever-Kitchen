{
    'name': 'Account Check Management',
    'version': '18.0.1.0.0',  # Odoo 18-compatible

    'category': 'Accounting',
    'sequence': 14,
    'summary': 'Manage check payments, returns, and checkbook tracking in accounting.',
    'description': """
Account Check Management
=========================

This module provides a full check lifecycle management system in Odoo Accounting, including:
- Issuing and printing checks
- Managing returned and under-collection checks
- Handling long-term and post-dated checks
- Custom check rejection flows

Changelog:
----------
- v1.0.0: Initial version for Odoo 15
- v1.1.0: Added 'Under Collection' check status
- v1.1.1: Included check data in payment printout
- v1.2.0: Introduced long-term check functionality
- v1.2.1: Used Check Payment Date instead of Issue Date
- v18.0.1.0.0: Ported and improved for Odoo 18

""",
    'author': "DigitalVizta",
    'website': "http://digitalvzita.com",

    'license': 'LGPL-3',
    'depends': ['account', 'accountant'],

    'data': [
        'security/account_check_security.xml',
        'security/ir.model.access.csv',
        'data/cron_jobs.xml',
        'wizard/check_action_view.xml',
        'wizard/view_check_reject.xml',
        'wizard/change_check_view.xml',
        'views/account_checkbook_view.xml',
        'views/account_check_view.xml',
        'views/account_view.xml',
        'views/account_voucher_view.xml',
        'views/account_check_templates.xml',
    ],

    'demo': [
        'data/data.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
