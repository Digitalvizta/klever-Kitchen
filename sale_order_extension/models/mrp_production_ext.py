from odoo import models, fields

class MrpProduction(models.Model):
    _inherit = 'mrp.production'


    production_date = fields.Datetime(string='Production Date')

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    main_bom = fields.Boolean(string="Main BOM")
