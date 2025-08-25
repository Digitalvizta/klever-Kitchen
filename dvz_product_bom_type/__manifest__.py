# -*- coding: utf-8 -*-
{
    'name': "Product BOM Type",

    'summary': "Adds a 'BOM' type flag to products with mutually exclusive selection logic.",

    'description': """
This module extends the product template model by adding an 'Is BOM' boolean field,
similar to 'Can be Sold' and 'Can be Purchased'. It enforces a constraint to allow
only one of these three flags to be selected at a time for a product.
    """,

    'author': "DigitalVizta",
    'website': "https://www.digitalvizta.com",

    'category': 'Product',
    'version': '1.0',

    'depends': ['stock'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/product_template_view.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': False,
}
