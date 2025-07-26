# -*- coding: utf-8 -*-
{
    'name': "Partner Pricelist Button",
    'summary': "Adds a smart button on customer form to view assigned pricelist",
    'description': """
This module adds a smart button to the res.partner (Customer) form view in Odoo,
allowing users to quickly access the customer's assigned pricelist.
    """,
    'author': "DigitalVizta",
    'website': "https://www.digitalvizta.com",
    'category': 'Sales',
    'version': '1.0',

    'depends': ['base', 'purchase'],

    'data': [
        'views/res_partner_view.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
