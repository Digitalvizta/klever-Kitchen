# -*- coding: utf-8 -*-
# from odoo import http


# class DvzSaleReport(http.Controller):
#     @http.route('/dvz_sale_report/dvz_sale_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dvz_sale_report/dvz_sale_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dvz_sale_report.listing', {
#             'root': '/dvz_sale_report/dvz_sale_report',
#             'objects': http.request.env['dvz_sale_report.dvz_sale_report'].search([]),
#         })

#     @http.route('/dvz_sale_report/dvz_sale_report/objects/<model("dvz_sale_report.dvz_sale_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dvz_sale_report.object', {
#             'object': obj
#         })

