# -*- coding: utf-8 -*-
# from odoo import http


# class DvzVendorProductData(http.Controller):
#     @http.route('/dvz_vendor_product_data/dvz_vendor_product_data', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dvz_vendor_product_data/dvz_vendor_product_data/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dvz_vendor_product_data.listing', {
#             'root': '/dvz_vendor_product_data/dvz_vendor_product_data',
#             'objects': http.request.env['dvz_vendor_product_data.dvz_vendor_product_data'].search([]),
#         })

#     @http.route('/dvz_vendor_product_data/dvz_vendor_product_data/objects/<model("dvz_vendor_product_data.dvz_vendor_product_data"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dvz_vendor_product_data.object', {
#             'object': obj
#         })

