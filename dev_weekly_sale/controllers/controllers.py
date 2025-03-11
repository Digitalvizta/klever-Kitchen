# -*- coding: utf-8 -*-
# from odoo import http


# class DevWeeklySale(http.Controller):
#     @http.route('/dev_weekly_sale/dev_weekly_sale', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dev_weekly_sale/dev_weekly_sale/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dev_weekly_sale.listing', {
#             'root': '/dev_weekly_sale/dev_weekly_sale',
#             'objects': http.request.env['dev_weekly_sale.dev_weekly_sale'].search([]),
#         })

#     @http.route('/dev_weekly_sale/dev_weekly_sale/objects/<model("dev_weekly_sale.dev_weekly_sale"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dev_weekly_sale.object', {
#             'object': obj
#         })

