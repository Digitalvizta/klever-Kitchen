# -*- coding: utf-8 -*-
{
    'name': "Weekly Batch Summary Report",
    'summary': "Generate weekly sales reports categorized by product.",
    'description': """
This module allows users to generate product-wise weekly sales reports 
based on sale orders within a given date range.
    """,
    'author': "DigitalVizta",
    'category': 'Sales',
    'version': '1.0',
    'license': 'LGPL-3',

    # Dependencies
    'depends': ['base', 'sale', 'dev_mrp_ext'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # Data
        'data/sequence_boms.xml',
        # Report
        'custom_wizard/report_action.xml',
        'custom_wizard/report_temp.xml',
        'custom_wizard/bom_report_action.xml',
        'custom_wizard/boms_report_temp.xml',

        # Views
        'views/boms.xml',
        'views/views.xml',

    ],
}
