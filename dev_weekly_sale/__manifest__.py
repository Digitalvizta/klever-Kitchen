# -*- coding: utf-8 -*-
{
    'name': "dev_weekly_sale",

    'summary': "Track weekly sales of products, displaying total quantities ordered per week.",

    'description': """
This module provides an easy way to track and visualize the total quantity of each product sold within a given week. 
It aggregates order quantities for products across sales orders, allowing users to view weekly sales performance.

Key features:
- Display weekly sales summary for each product.
- Show the total quantity sold for each product per week.
- Easy-to-use interface for tracking and analyzing product sales over time.

This module is useful for sales teams and managers to analyze the sales performance of products on a weekly basis.
    """,

    'author': "DigitalVizta",
    'website': "https://www.digitalvizta.com",

    # Categories can be used to filter modules in the modules listing
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'security/ir.model.access.csv',
        'report/report_weekly_sales_template.xml',
        'wizard/weekly_sales_report_wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
