# -*- coding: utf-8 -*-
{
    'name': "Partner Role Management",

    'summary': "Manage and restrict partner roles to a single selection: Customer, Vendor, Both, or Employee.",

    'description': """
This module enhances the res.partner model by adding role flags (Customer, Vendor, Both, Employee) 
and enforces a constraint that only one role can be selected per partner. It also includes 
onchange behavior to automatically deselect other roles when one is chosen.
    """,

    'author': "DigitalVizta",
    'website': "https://www.digitalvizta.com",

    'category': 'Contacts',
    'version': '0.1',

    'depends': ['base','dvz_partner_type_flags'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/res_partner_view.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
}
