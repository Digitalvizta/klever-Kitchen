# -*- coding: utf-8 -*-
# from odoo import http


# class DvzVendorProductExt(http.Controller):
#     @http.route('/dvz_vendor_product_ext/dvz_vendor_product_ext', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dvz_vendor_product_ext/dvz_vendor_product_ext/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dvz_vendor_product_ext.listing', {
#             'root': '/dvz_vendor_product_ext/dvz_vendor_product_ext',
#             'objects': http.request.env['dvz_vendor_product_ext.dvz_vendor_product_ext'].search([]),
#         })

#     @http.route('/dvz_vendor_product_ext/dvz_vendor_product_ext/objects/<model("dvz_vendor_product_ext.dvz_vendor_product_ext"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dvz_vendor_product_ext.object', {
#             'object': obj
#         })

