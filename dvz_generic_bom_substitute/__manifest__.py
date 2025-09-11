# -*- coding: utf-8 -*-
{
    'name': "Generic BOM Substitute",

    'summary': "Substitute generic BoM components with actual inventory products using FIFO",

    'description': """
This module allows manufacturers to define generic placeholder products (e.g., "Salt") in a Bill of Materials (BoM), 
and automatically substitute them during manufacturing with linked physical inventory items (e.g., Salt 1, Salt 2) 
using FIFO logic. This ensures accurate inventory tracking, flexibility in raw material usage, 
and maintains clean BoMs without hardcoding specific vendor products.
    """,

    'author': "DigitalVizta",
    'website': "https://www.digitalvizta.com",

    'category': 'Manufacturing',
    'version': '0.1',

    'depends': [
        'base',
        'stock',
        'mrp',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml'
    ],

    'demo': [
        # 'demo/demo.xml',
    ],

    'application': False,
    'installable': True,
    'auto_install': False,
}
