# -*- coding: utf-8 -*-
{
    'name': "DVZ Sale Report",

    'summary': "Provides enhanced sales reporting functionality",

    'description': """
This module adds custom sales reports and related views to improve visibility and analysis of sales data.
    """,

    'author': "DigitalVizta",
    'website': "https://www.digitalvizta.com",

    'category': 'Sales',
    'version': '0.1',

    # Required dependencies for this module
    'depends': ['base','customer_weekly_sales_report', 'print_sale_order_from_wizard', 'product_vise_sale_order_report'],

    # Data files always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],

    # Demo data for demonstration purposes only
    'demo': [
        'demo/demo.xml',
    ],
}
