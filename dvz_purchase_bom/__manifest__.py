# -*- coding: utf-8 -*-
{
    'name': "Weekly Purchase Summary Report",
    'summary': "Generate weekly sales reports categorized by product.",
    'description': """
This module allows users to generate product-wise weekly sales reports 
based on sale orders within a given date range..
    """,
    'author': "DigitalVizta",
    'category': 'Sales',
    'version': '1.0',
    'license': 'LGPL-3',

    # Dependencies
    'depends': ['base', 'sale', 'mrp'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'custom_wizard/report_action.xml',
        'custom_wizard/report_temp.xml',
    ],
}
