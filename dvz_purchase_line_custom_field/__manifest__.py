# -*- coding: utf-8 -*-
{
    'name': "Purchase Line Custom Field",

    'summary': "Adds a custom field next to Product in Purchase Order Line",

    'description': """
This module extends the purchase order line to include a custom field beside the product field.
Useful for adding extra product-related input or selection in the purchase process.
    """,

    'author': "DigitalVizta",
    'website': "https://www.digitalvizta.com",

    'category': 'Purchases',
    'version': '1.0',

    'depends': ['purchase'],

    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_views.xml',
        'views/vendor_master_views.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
