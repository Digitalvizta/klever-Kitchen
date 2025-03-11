# -*- coding: utf-8 -*-
{
    'name': "Print Sale Orders From Wizard",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Jamshad Khan",
    'category': 'sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'custom_wizard/report_action.xml',
        'custom_wizard/report_temp.xml',
    ],
}

