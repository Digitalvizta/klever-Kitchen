# -*- coding: utf-8 -*-
{
    'name': "Vendor Product Extension",
    'summary': "Enhance product templates with vendor, inventory, and manufacturer details",
    'description': """
Vendor Product Extension
=====================================

This module extends the standard Product Template in Odoo by adding vendor, 
inventory, and manufacturer-specific fields to support better product tracking 
and compliance.

Key Features:
-------------
- Vendor Information:
  • Vendor SKU, Pack Size, Pack UOM
  • Layers per Pallet, Items per Pallet Layer
  • Delivery Lead Time

- Inventory Extensions:
  • Predefined Inventory Locations (Coolers, Freezers, Dry Goods, etc.)

- Manufacturer Information:
  • Ingredients, Storage Location
  • Shelf Life, Lot Number, Expiration Date
  • Document Uploads: Spec Sheets, Nutrition Facts, Allergen Statements, COAs
    """,
    'author': "DigitalVizta",
    'website': "https://www.digitalvizta.com",
    'category': 'Product',
    'version': '1.0',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/product_category_type_view.xml',
        'views/product_supplierinfo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
