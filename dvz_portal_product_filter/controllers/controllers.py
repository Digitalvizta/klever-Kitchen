# -*- coding: utf-8 -*-
# from odoo import http


# class DvzPortalProductFilter(http.Controller):
#     @http.route('/dvz_portal_product_filter/dvz_portal_product_filter', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dvz_portal_product_filter/dvz_portal_product_filter/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dvz_portal_product_filter.listing', {
#             'root': '/dvz_portal_product_filter/dvz_portal_product_filter',
#             'objects': http.request.env['dvz_portal_product_filter.dvz_portal_product_filter'].search([]),
#         })

#     @http.route('/dvz_portal_product_filter/dvz_portal_product_filter/objects/<model("dvz_portal_product_filter.dvz_portal_product_filter"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dvz_portal_product_filter.object', {
#             'object': obj
#         })

