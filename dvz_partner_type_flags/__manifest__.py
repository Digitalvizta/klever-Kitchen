# -*- coding: utf-8 -*-
{
    'name': "Partner Customer/Vendor Flags",

    'summary': "Manually manage Customer, Vendor, and Both flags on partner records",

    'description': """
This module adds three manual boolean fields on partner form: 
- Is Customer
- Is Vendor
- Is Customer & Vendor

These flags help easily identify partner types in the form view and filter them in the list view.
    """,

    'author': "DigitalVizta",
    'website': "https://www.digitalvizta.com",

    'category': 'Contacts',
    'version': '1.0',

    'depends': ['base'],

    'data': [
        'views/res_partner.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
