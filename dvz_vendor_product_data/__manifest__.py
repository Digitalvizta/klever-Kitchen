# -*- coding: utf-8 -*-
{
    'name': "Vendor Product Data",

    'summary': "Manage vendor-specific product data with pricing and availability",

    'description': """
This module allows you to maintain vendor-specific product information, including pricing,
minimum quantities, delivery delays, product codes, and availability periods.
It extends the product and vendor relationship for use in the purchasing workflow.
    """,

    'author': "DigitalVizta",
    'website': "https://www.digitalvizta.com",

    'category': 'Purchases',
    'version': '1.0',

    # Dependencies for proper integration with product and purchase modules
    'depends': [
        'base',
        'purchase',
        'product',
    ],

    # Always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/vendor_product_views.xml',
        # 'security/ir.model.access.csv',  # Uncomment after adding access rights
    ],

    # Demo data (optional)
    'demo': [
        'demo/demo.xml',
    ],

    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
