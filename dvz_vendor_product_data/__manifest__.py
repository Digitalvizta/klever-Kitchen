# -*- coding: utf-8 -*-
{
    'name': "Vendor Product Data",
    'summary': "Manage and organize vendor-specific product information.",
    'description': """
        Vendor Product Data Module by DigitalVizta.

        This module enables the management of product information tied to specific vendors.
        It is useful for procurement processes, vendor management, and maintaining accurate product listings.
    """,
    'author': "DigitalVizta",
    'website': "https://www.digitalvizta.com",
    'category': 'Inventory',
    'version': '1.0.0',
    'license': 'LGPL-3',

    # Dependencies
    'depends': ['base','purchase','stock'],

    # Data files loaded automatically
    'data': [
        'security/ir.model.access.csv',
        'views/vendor_master_views.xml',
    ],

    # Demo data (optional)
    'demo': [
        'demo/demo.xml',
    ],
}
