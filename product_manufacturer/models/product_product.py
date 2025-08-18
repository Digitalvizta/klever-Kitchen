# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    manufacturer_id = fields.Many2one(comodel_name="res.partner", string="Manufacturer")
    manufacturer_pname = fields.Char(string="Manufacturer Product Name")
    manufacturer_pref = fields.Char(string="Manufacturer BAR Code")
    manufacturer_brand = fields.Char(string="Brand")
    manufacturer_purl = fields.Char(string="Manufacturer Product URL")
    manufacturer_des = fields.Text(string="Description")
    allgern_statement = fields.Char(string="Allgern Statement")
    storage_tempature = fields.Char(string="Storage Tempature")
    manufacturer_sku = fields.Char(string="Manufacturer SKU")
