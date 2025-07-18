# -*- coding: utf-8 -*-
{
    'name': "Sale Order Extension",

    'summary': "Adds custom fields (Pick Up Date, PO No, BOL, Lot No) to Sale Order form",

    'description': """
This module extends the Sale Order model to include additional fields such as:
- Pick Up Date (Datetime)
- PO No. (Char)
- BOL (Bill of Lading) (Char)
- Lot No. (Char)

These fields help capture essential logistics and order-related information.
    """,

    'author': "DigitalVizta",
    'website': "https://www.digitalvizta.com",

    'category': 'Sales',
    'version': '18.0.1.0.0',

    'depends': ['sale_management'],

    'data': [
        'views/sale_order_view.xml',
        'views/mrp_production_view.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
