# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "All In One Sale Reports",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Sales",
    "summary": """Sales Report Based On Analysis Compare Customer By Sales Report Module Compare Products Based On Selling Salesperson Wise Payment Report Sales Report By Customer And Sales Person Sales Report By Tax All in one sales report Odoo Days Wise Product Sales Report Sales Details Report Sale Report by Salesperson Invoice Payment Report Top Customer Sale order Product Profit Report Sale order Invoice Summary Product Indent Report Sale order By Category Report Top Selling Product Dynamic Hourly Sales Report Customer Sales Analysis Report Sales Sector Report Customer Sale order Analysis Sales Product Profit Report Sales Invoice Summary Product Sales Indent Report Sales By Category Report Product Attribute Wise Sales Report Sale order Details Report Sale order Report by Salesperson Invoices Payment Report Top Customers Sale order Products Profit Report Sale orders Invoice Summary Products Indent Report Sale orders By Category Report Top Selling Products Dynamic Hourly Sale Report Customer Sales Analysis Report Sector wise Sales Report Customer Sale orders Analysis Sales Products Profit Report Sales Invoices Summary Product Sales wise Indent Report Product Attributes Wise Sales Report""",
    "description": """ All in one sale report useful to provide different sales and invoice reports to do analysis. A sales analysis report shows the trends that occur in a company's sales volume over time. In its most basic form, a sales analysis report shows whether sales are increasing or declining. At any time during the fiscal year, sales managers may analyze the trends in the report to determine the best course of action. Sales reports are a record of sales activity over a particular period. These reports detail what reps have been up to, reveal whether the team is on track to meet its quota, and alert management to any potential issues.
Sales Report Based On Analysis, Compare Customer By Sales Report Module, Compare Products Based On Selling, Salesperson Wise Payment Report, Sales Report By Customer And Sales Person, Sales Report By Tax, Sale Report By Date And Time Odoo """,
    "version": "0.0.1",
    "depends": [
                "sale_management",
    ],
    "application": True,
    "data": [
        "security/sh_sale_reports_groups.xml",

        'sh_customer_sales_analysis/security/ir.model.access.csv',
        'sh_customer_sales_analysis/report/report_sales_analysis_views.xml',
        'sh_customer_sales_analysis/wizard/customer_sales_analysis_wizard_views.xml',
        'sh_customer_sales_analysis/views/sh_customer_sales_analysis_views.xml',

        'sh_day_wise_sales/security/ir.model.access.csv',
        'sh_day_wise_sales/wizard/sale_order_day_wise_wizard_views.xml',
        'sh_day_wise_sales/report/sale_order_day_wise_report_views.xml',
        'sh_day_wise_sales/views/sh_day_wise_sales_views.xml',

        "sh_payment_report/security/ir.model.access.csv",
        "sh_payment_report/wizard/payment_report_wizard_views.xml",
        "sh_payment_report/report/payment_report_views.xml",
        "sh_payment_report/views/sh_payment_report_views.xml",

        'sh_product_sales_indent/security/ir.model.access.csv',
        'sh_product_sales_indent/report/sh_report_sales_product_indent_templates.xml',
        'sh_product_sales_indent/wizard/sh_sale_product_indent_wizard_views.xml',
        'sh_product_sales_indent/views/sh_product_sales_indent_views.xml',

        'sh_sale_by_category/security/ir.model.access.csv',
        'sh_sale_by_category/report/sh_sale_by_category_templates.xml',
        'sh_sale_by_category/wizard/sh_sale_by_category_wizard_views.xml',
        'sh_sale_by_category/views/sh_sale_by_product_category_views.xml',

        "sh_sale_details_report/security/ir.model.access.csv",
        "sh_sale_details_report/wizard/sh_sale_details_report_wizard_views.xml",
        "sh_sale_details_report/report/sh_sale_details_templates.xml",
        "sh_sale_details_report/views/sh_sale_details_views.xml",

        'sh_sale_invoice_summary/security/ir.model.access.csv',
        'sh_sale_invoice_summary/report/sh_sale_invoice_summary_report_templates.xml',
        'sh_sale_invoice_summary/wizard/sh_sale_invoice_summary_wizard_views.xml',
        'sh_sale_invoice_summary/views/sh_sale_invoice_summary_views.xml',

        'sh_sale_product_attribute_report/security/ir.model.access.csv',
        'sh_sale_product_attribute_report/report/sh_sale_product_attribute_report_templates.xml',
        'sh_sale_product_attribute_report/report/sh_sale_product_attribute_reports.xml',
        'sh_sale_product_attribute_report/wizard/sh_sale_product_attribute_wizard_views.xml',

        'sh_sale_product_profit/security/ir.model.access.csv',
        'sh_sale_product_profit/data/sale_order_data.xml',
        'sh_sale_product_profit/report/sh_sales_product_profit_templates.xml',
        'sh_sale_product_profit/wizard/sh_sales_product_profit_wizard_views.xml',
        'sh_sale_product_profit/views/sale_order_line_views.xml',
        'sh_sale_product_profit/views/sh_sale_product_profit_views.xml',

        "sh_sale_report_salesperson/security/ir.model.access.csv",
        "sh_sale_report_salesperson/wizard/sh_salesperson_wizard_views.xml",
        "sh_sale_report_salesperson/report/sh_salesperson_report_templates.xml",
        "sh_sale_report_salesperson/views/sh_sale_report_salesperson_views.xml",

        'sh_sale_sector_report/security/ir.model.access.csv',
        'sh_sale_sector_report/wizard/sector_report_wizard_views.xml',
        'sh_sale_sector_report/views/sector_views.xml',

        "sh_top_customers/security/ir.model.access.csv",
        "sh_top_customers/wizard/sh_top_customer_wizard_views.xml",
        "sh_top_customers/report/sh_top_customer_templates.xml",
        "sh_top_customers/views/sh_top_customer_views.xml",

        "sh_top_selling_product/security/ir.model.access.csv",
        "sh_top_selling_product/wizard/sh_top_selling_wizard_views.xml",
        "sh_top_selling_product/views/sh_top_selling_views.xml",
        "sh_top_selling_product/report/sh_top_selling_product_temlates.xml",

    ],
    "images": ["static/description/background.gif", ],
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
    "price": 100,
    "currency": "EUR"
}
