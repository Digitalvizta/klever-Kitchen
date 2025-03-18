# -*- coding: utf-8 -*-
# from odoo import http


# class CustomerWeeklySalesReport(http.Controller):
#     @http.route('/customer_weekly_sales_report/customer_weekly_sales_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customer_weekly_sales_report/customer_weekly_sales_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('customer_weekly_sales_report.listing', {
#             'root': '/customer_weekly_sales_report/customer_weekly_sales_report',
#             'objects': http.request.env['customer_weekly_sales_report.customer_weekly_sales_report'].search([]),
#         })

#     @http.route('/customer_weekly_sales_report/customer_weekly_sales_report/objects/<model("customer_weekly_sales_report.customer_weekly_sales_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customer_weekly_sales_report.object', {
#             'object': obj
#         })

