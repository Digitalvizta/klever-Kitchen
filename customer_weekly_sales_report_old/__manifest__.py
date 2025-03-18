{
    'name': 'Customer Weekly Sales Report',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Generate a weekly sales report grouped by customers',
    'author': 'Jamshad Khan',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/report_wizard_views.xml',
        'views/customer_sales_report.xml',
    ],
    'installable': True,
    'application': False,
}
