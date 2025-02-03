# -*- coding: utf-8 -*-
{
    'name': "Dev MRP EXT",
    'summary': "Customizations for batch output in manufacturing",
    'description': """
    This module customizes the manufacturing process in Odoo to include batch output features. It provides an interface for batch production, tracking, and reporting within the manufacturing process.
    """,
    'author': "DigitalVizta",
    'website': "https://www.DigitalVizta.com",
    'category': 'Manufacturing',
    'version': '0.1',
    'depends': ['base', 'mrp'],  # The 'mrp' module is crucial for Manufacturing-related customizations.
    'data': [
        # Security file to manage access rights (if needed)
        # 'security/ir.model.access.csv',

        # Define your views, templates, and menus for batch output
        # 'views/mrp_production_views.xml',  # Custom views for batch production and output.
        'views/templates.xml',  # Additional templates if needed.
        'views/views.xml',  # Additional templates if needed.
    ],
    'demo': [
        'demo/demo.xml',  # Demo data if you want to include some sample data for testing
    ],
    'application': True,  # Makes the module available in the Apps menu
    'installable': True,  # Set to False if you don't want the module to be installable in production
    'auto_install': False,  # Whether the module should be automatically installed
}
