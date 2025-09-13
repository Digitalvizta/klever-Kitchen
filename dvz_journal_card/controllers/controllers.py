# -*- coding: utf-8 -*-
# from odoo import http


# class DvzJournalCard(http.Controller):
#     @http.route('/dvz_journal_card/dvz_journal_card', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dvz_journal_card/dvz_journal_card/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dvz_journal_card.listing', {
#             'root': '/dvz_journal_card/dvz_journal_card',
#             'objects': http.request.env['dvz_journal_card.dvz_journal_card'].search([]),
#         })

#     @http.route('/dvz_journal_card/dvz_journal_card/objects/<model("dvz_journal_card.dvz_journal_card"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dvz_journal_card.object', {
#             'object': obj
#         })

