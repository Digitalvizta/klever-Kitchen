# -*- coding: utf-8 -*-
# from odoo import http


# class WizardReport(http.Controller):
#     @http.route('/wizard_report/wizard_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wizard_report/wizard_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('wizard_report.listing', {
#             'root': '/wizard_report/wizard_report',
#             'objects': http.request.env['wizard_report.wizard_report'].search([]),
#         })

#     @http.route('/wizard_report/wizard_report/objects/<model("wizard_report.wizard_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wizard_report.object', {
#             'object': obj
#         })

