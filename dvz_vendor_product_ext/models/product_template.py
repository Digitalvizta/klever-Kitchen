# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # General
    description = fields.Text(string="Description")
    sub_category_id = fields.Many2one(
        'product.category',
        string="Sub-Category"
    )
    tag_ids = fields.Many2many(
        'product.tag',
        'product_template_tag_rel',
        'product_tmpl_id',
        'tag_id',
        string="Tags"
    )

    # Vendor
    vendor_sku = fields.Char(string="Vendor SKU")
    vendor_pack_size = fields.Float(string="Vendor Pack Size")
    vendor_pack_size_uom = fields.Many2one('uom.uom', string="Vendor Pack Size UOM")
    layers_per_pallet = fields.Integer(string="Layers per Pallet")
    items_per_pallet_layer = fields.Integer(string="Items per Pallet Layer")
    delivery_lead_time = fields.Integer(string="Delivery Lead Time (days)")

    # Inventory
    inventory_location = fields.Selection(
        selection=[
            ('finished_goods_cooler_1', 'Finished Goods Cooler 1'),
            ('finished_goods_cooler_2', 'Finished Goods Cooler 2'),
            ('raw_material_cooler_3', 'Raw Material Cooler 3'),
            ('freezer_1', 'Freezer 1'),
            ('red_meat_1', 'Red Meat 1'),
            ('poultry_1', 'Poultry 1'),
            ('dry_goods_1', 'Dry Goods 1'),
            ('chemical_station_1', 'Chemical Station 1'),
            ('tool_station_1', 'Tool Station 1'),
            ('shipping_station_1', 'Shipping Station 1'),
            ('front_office_1', 'Front Office 1'),
            ('stock_room_1', 'Stock Room 1'),
            ('employee_room_1', 'Employee Room 1'),
            ('main_floor', 'Main Floor'),
            ('semi_finished_goods_1', 'Semi-Finished Goods Location 1'),
        ],
        string="Inventory Location"
    )

    # Manufacturer
    ingredients = fields.Text(string="Ingredients")
    storage_location = fields.Selection(
        selection=[('dry_goods', 'Dry Goods'), ('cooler', 'Cooler'), ('freezer', 'Freezer')],
        string="Storage Location"
    )
    shelf_life = fields.Char(string="Shelf Life")
    lot_number = fields.Char(string="Lot Number")
    expiration_date = fields.Date(string="Expiration Date")

    manufacturer_id = fields.Many2one(comodel_name="res.partner", string="Manufacturer")
    manufacturer_pname = fields.Char(string="Manufacturer Product Name")
    manufacturer_pref = fields.Char(string="Manufacturer BAR Code")
    manufacturer_brand = fields.Char(string="Brand")
    manufacturer_purl = fields.Char(string="Manufacturer Product URL")
    manufacturer_des = fields.Text(string="Description")
    allgern_statement = fields.Char(string="Allgern Statement")
    storage_tempature = fields.Char(string="Storage Tempature")
    manufacturer_sku = fields.Char(string="Manufacturer SKU")

    # Manufacturer Documents Uploads with filenames
    specification_sheet = fields.Binary(string="Specification Sheet")
    specification_sheet_fname = fields.Char(string="Spec Sheet Filename")

    nutrition_facts = fields.Binary(string="Nutrition Facts")
    nutrition_facts_fname = fields.Char(string="Nutrition Facts Filename")

    allergen_statement = fields.Binary(string="Allergen Statement")
    allergen_statement_fname = fields.Char(string="Allergen Statement Filename")

    coa_document = fields.Binary(string="COA")
    coa_document_fname = fields.Char(string="COA Filename")
