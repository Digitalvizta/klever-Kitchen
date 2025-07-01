# -*- coding: utf-8 -*-
{
    'name': 'Purchase Product Vendor Filter',
    'version': '1.0',
    'category': 'Purchases',
    'author': 'DigitalVizta',
    'website': 'https://digitalvizta.com',
    'summary': 'Filter products in Purchase Order based on selected Vendor',
    'description': """
        This module filters the product list in purchase order lines..
        - If no vendor is selected: show all products.
        - If a vendor is selected: show only products where the vendor is listed in the product's purchase tab.
    """,
    'depends': ['purchase','stock'],
    'data': [
        'views/purchase_order.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

