# -*- coding: utf-8 -*-
# from odoo import http


# class DevMrpExt(http.Controller):
#     @http.route('/dev_mrp_ext/dev_mrp_ext', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dev_mrp_ext/dev_mrp_ext/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dev_mrp_ext.listing', {
#             'root': '/dev_mrp_ext/dev_mrp_ext',
#             'objects': http.request.env['dev_mrp_ext.dev_mrp_ext'].search([]),
#         })

#     @http.route('/dev_mrp_ext/dev_mrp_ext/objects/<model("dev_mrp_ext.dev_mrp_ext"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dev_mrp_ext.object', {
#             'object': obj
#         })

