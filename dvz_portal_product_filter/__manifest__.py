# -*- coding: utf-8 -*-
{
    'name': "DVZ Portal Product Filter",
    'version': '18.0.1.0.0',
    'category': 'Website',
    'summary': "Restrict portal users to view only their assigned or related products on the website",
    'description': """
This module customizes the website product listing to ensure that
portal users (customers) only see products relevant to them.

Key Features:
--------------------------------------------------
- Adds a Many2many field “Allowed Customers” on products
- Restricts product visibility on the website based on the logged-in user
- Optional record rule for deeper access control
- Supports B2B or restricted catalog environments
    """,
    'author': "DigitalVizta",
    'website': "https://www.digitalvizta.com",
    'license': 'LGPL-3',

    # Dependencies
    'depends': [
        'website_sale',
        'sale',
        'portal',
    ],

    # Data files (uncomment if you include these)
    'data': [
        'security/ir_rule.xml',
        # 'security/ir.model.access.csv',
        # 'views/product_template_views.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
