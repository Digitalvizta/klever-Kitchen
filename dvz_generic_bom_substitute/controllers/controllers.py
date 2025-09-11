# -*- coding: utf-8 -*-
# from odoo import http


# class DvzGenericBomSubstitute(http.Controller):
#     @http.route('/dvz_generic_bom_substitute/dvz_generic_bom_substitute', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dvz_generic_bom_substitute/dvz_generic_bom_substitute/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dvz_generic_bom_substitute.listing', {
#             'root': '/dvz_generic_bom_substitute/dvz_generic_bom_substitute',
#             'objects': http.request.env['dvz_generic_bom_substitute.dvz_generic_bom_substitute'].search([]),
#         })

#     @http.route('/dvz_generic_bom_substitute/dvz_generic_bom_substitute/objects/<model("dvz_generic_bom_substitute.dvz_generic_bom_substitute"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dvz_generic_bom_substitute.object', {
#             'object': obj
#         })

