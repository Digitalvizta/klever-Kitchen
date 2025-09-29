# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from fractions import Fraction


BOX_TYPE_SELECTION = [
    ('retail_box', 'Retail Box 9 7/8 x 9 7/8 x 6 1/8 (2/5 LB)'),
    ('fsh_box', 'FSH Box 12 5/8 x 10 7/16 x 6 5/8 (2/10 LB & 2 Trays)'),
    ('clamshell_full', 'Full Size Clamshell 19 3/8 x 11 1/2 x 5 7/8 (24/12 oz & 16/16 oz)'),
    ('12_layer_patty', '12 Layer Patty Box 17 1/4 x 13 1/4 x 5 1/4 (120)'),
]

NET_WEIGHT_UOM = [
    ('oz', 'OZ'),
    ('lb', 'LB'),
]

PACK_UOM_SELECTION = [
    ('oz','OZ'), ('lb','LB'), ('gal','GAL'), ('ea','EA'),
    ('pk','PK'), ('l','L'), ('ct','CT')
]

PACK_CONTAINER_SELECTION = [
    ('cs','CS'), ('pail','Pail'), ('bags','Bags'),
    ('tote', 'Tote'), ('lb', 'LB'), ('ea', 'EA')
]

BASIC_PREP_OPTIONS = [
    ('best_before', 'Best Before Date'),
    ('expiration', 'Expiration Date'),
    ('packaging', 'Packaging Date'),
    ('production', 'Production Date'),
    ('use_by', 'Use By Date'),
]


class ProductAllergen(models.Model):
    _name = 'product.allergen'
    _description = 'Product Allergen (simple lookup)'

    name = fields.Char(required=True)
    code = fields.Char()


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # ---------------------------
    # GENERAL
    # ---------------------------
    description = fields.Text(string='Description')
    sub_category_id = fields.Many2one('product.category', string="Sub-Category")

    tag_ids = fields.Many2many(
        'product.tag',
        'product_template_tag_rel',
        'product_tmpl_id',
        'tag_id',
        string='Tags'
    )


    information_owner_gln = fields.Char(
        string='Information Owner GLN',
        size=15,
        help='15 numeric chars (GLN)'
    )

    shelf_life_days = fields.Integer(
        string='Shelf Life (Days)',
        help='Enter number of days (0-999)'
    )

    # old text allergen statement
    allergen_statement_text = fields.Char(string='Allergen Statement', size=200)

    contains_ids = fields.Many2many(
        'product.allergen',
        'product_template_allergen_rel',
        'product_tmpl_id',
        'allergen_id',
        string='Contains',
        help='Select allergens that apply (Milk, Eggs, Fish, ...)'
    )

    # Detail fields for certain allergens
    fish_type = fields.Char(string='Fish Type')
    crustacean_type = fields.Char(string='Crustacean Shellfish Type')
    tree_nut_type = fields.Char(string='Tree Nut Type')

    # Attachments (generic)
    attachment_ids = fields.One2many(
        'ir.attachment',
        'res_id',
        domain=[('res_model', '=', 'product.template')],
        string='Attachments'
    )

    # ---------------------------
    # MANUFACTURER
    # ---------------------------
    product_category_type = fields.Many2one('product.category.type', string="Product Category type")
    auto_code = fields.Char(string="Auto Sequence Code", readonly=False, copy=False)
    manufacturer_id = fields.Many2one('res.partner', string="Manufacturer")
    manufacturer_pname = fields.Char(string="Manufacturer Product Name")
    manufacturer_pref = fields.Char(string="Manufacturer Bar Code")
    manufacturer_brand = fields.Char(string="Brand")
    manufacturer_purl = fields.Char(string="Manufacturer Product URL")
    manufacturer_description = fields.Text(string="Manufacturer Description")
    previous_manufacturer_code = fields.Char(string="Previous Manufacturer Code")

    # from old version
    shelf_life = fields.Char(string="Shelf Life")
    lot_number = fields.Char(string="Lot Number")
    expiration_date = fields.Date(string="Expiration Date")
    storage_temperature = fields.Char(string="Storage Temperature")

    ingredients = fields.Text(string="Ingredients")

    # Manufacturer documents
    specification_sheet = fields.Binary(string="Specification Sheet")
    specification_sheet_fname = fields.Char(string="Spec Sheet Filename")

    nutrition_facts = fields.Binary(string="Nutrition Facts")
    nutrition_facts_fname = fields.Char(string="Nutrition Facts Filename")

    allergen_statement = fields.Binary(string="Allergen Statement")
    allergen_statement_fname = fields.Char(string="Allergen Statement Filename")

    coa_document = fields.Binary(string="COA")
    coa_document_fname = fields.Char(string="COA Filename")

    barcode_image = fields.Binary(string='Bar Code Image')
    barcode_image_fname = fields.Char(string='Bar Code Image Filename')

    label_image = fields.Binary(string='Label Image')
    label_image_fname = fields.Char(string='Label Image Filename')

    trade_item_date_on_pack_type = fields.Selection(
        selection=BASIC_PREP_OPTIONS,
        string='Trade Item Date On Packaging Type Code'
    )

    # ---------------------------
    # PURCHASE
    # ---------------------------
    vendor_id = fields.Many2one('res.partner', string='Vendor')
    vendor_product_name = fields.Char(string='Vendor Product')
    vendor_sku = fields.Char(string='Vendor SKU')
    vendor_delivery_lead_time = fields.Integer(string='Vendor Delivery Lead Time (days)')

    # missing vendor fields restored
    vendor_pack_size = fields.Float(string="Vendor Pack Size")
    vendor_pack_size_uom = fields.Many2one('uom.uom', string="Vendor Pack Size UOM")

    purchase_price = fields.Float(string='Purchase Price')

    # ---------------------------
    # SALES
    # ---------------------------
    standard_price = fields.Float(string='Cost')   # Odoo's standard cost
    list_price = fields.Float(string='Sales Price')

    # ---------------------------
    # PACKAGING ATTRIBUTES
    # ---------------------------
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

    pack_size_qty_1 = fields.Integer(string='Pack Size Qty 1')
    pack_size_qty_2 = fields.Integer(string='Pack Size Qty 2')
    pack_size_uom = fields.Selection(PACK_UOM_SELECTION, string='Pack Size UoM')
    pack_container_type = fields.Selection(PACK_CONTAINER_SELECTION, string='Pack Container Type')
    pack_size_display = fields.Char(string='Pack Size Display', compute='_compute_pack_display')

    net_weight = fields.Float(string='Net Weight')
    net_weight_uom = fields.Selection(NET_WEIGHT_UOM, string='Net Weight UoM', help='Net weight excludes packaging')
    box_type = fields.Selection(BOX_TYPE_SELECTION, string='Box Type')

    # Fraction-capable dimensions (preferred)
    package_height = fields.Char(string='Package Height (IN)')
    package_depth = fields.Char(string='Package Depth (IN)')
    package_width = fields.Char(string='Package Width (IN)')
    pallet_height = fields.Char(string='Pallet Height (IN)')

    # Old float dimension fields (kept for compatibility)
    package_height_in = fields.Float(string='Package Height (Float IN)')
    package_depth_in = fields.Float(string='Package Depth (Float IN)')
    package_width_in = fields.Float(string='Package Width (Float IN)')
    pallet_height_in = fields.Float(string='Pallet Height (Float IN)')

    package_weight = fields.Float(string='Package Weight (gross)')
    package_weight_uom = fields.Selection(NET_WEIGHT_UOM, string='Package Weight UoM')

    layers_per_pallet = fields.Integer(string='Layers Per Pallet')
    items_per_layer = fields.Integer(string='Items Per Layer')

    package_cubic_feet = fields.Float(string='Package Cubic Feet', compute='_compute_package_cubic_feet', store=True)

    # ---------------------------
    # MARKETING
    # ---------------------------
    brand_name = fields.Char(string='Brand Name')
    marketing_message = fields.Text(string='Marketing Message', size=1000)
    basic_preparation_text = fields.Char(string='Basic Preparation', size=500)
    serving_information = fields.Text(string='Serving Information', size=1000)

    pos_image = fields.Binary(string='POS Image')
    pos_image_fname = fields.Char(string='POS Filename')

    formulation_statement_1 = fields.Binary(string='Product Formulation Statement 1')
    formulation_statement_1_fname = fields.Char(string='Formulation 1 Filename')

    formulation_statement_2 = fields.Binary(string='Product Formulation Statement 2')
    formulation_statement_2_fname = fields.Char(string='Formulation 2 Filename')

    # ---------------------------
    # MISC / IDENTIFIERS / LOCKS
    # ---------------------------
    auto_sequence_code = fields.Char(string='Auto Sequence Code', size=4, help='4 digit auto sequence code')
    barcode = fields.Char(string='Bar Code')

    _LOCKED_AFTER_CREATE = [
        'sale_ok', 'purchase_ok', 'type', 'categ_id', 'auto_sequence_code', 'barcode'
    ]

    # ---------------------------
    # COMPUTE / CONSTRAINTS
    # ---------------------------
    @api.depends('pack_size_qty_1', 'pack_size_qty_2', 'pack_size_uom', 'pack_container_type')
    def _compute_pack_display(self):
        for rec in self:
            parts = []
            if rec.pack_size_qty_1:
                parts.append(str(rec.pack_size_qty_1))
            if rec.pack_size_qty_2:
                parts.append(str(rec.pack_size_qty_2))
            if rec.pack_size_uom:
                parts.append(rec.pack_size_uom.upper())
            if rec.pack_container_type:
                parts.append(rec.pack_container_type.upper())
            rec.pack_size_display = ' / '.join(parts) if parts else False

    def _frac_to_float(self, s):
        if not s:
            return None
        s = s.strip()
        try:
            if ' ' in s:
                whole, frac = s.split(' ', 1)
                return float(int(whole) + Fraction(frac))
            if '/' in s:
                return float(Fraction(s))
            return float(s)
        except Exception:
            return None

    @api.depends('package_height', 'package_width', 'package_depth')
    def _compute_package_cubic_feet(self):
        for rec in self:
            h = self._frac_to_float(rec.package_height)
            w = self._frac_to_float(rec.package_width)
            d = self._frac_to_float(rec.package_depth)
            if h is None or w is None or d is None:
                rec.package_cubic_feet = 0.0
            else:
                rec.package_cubic_feet = round((h * w * d) / 1728.0, 6)

    @api.constrains('information_owner_gln')
    def _check_gln(self):
        for rec in self:
            if rec.information_owner_gln and len(rec.information_owner_gln) != 15:
                raise ValidationError(_("Information Owner GLN must be exactly 15 characters."))

    @api.constrains('shelf_life_days')
    def _check_shelf_life(self):
        for rec in self:
            if rec.shelf_life_days and (rec.shelf_life_days < 0 or rec.shelf_life_days > 999):
                raise ValidationError(_("Shelf life must be 0-999 days."))

    @api.onchange('contains_ids')
    def _onchange_contains_ids(self):
        names = self.contains_ids.mapped('name') if self.contains_ids else []
        if 'Fish' not in names:
            self.fish_type = False
        if 'Crustacean Shellfish' not in names:
            self.crustacean_type = False
        if 'Tree Nuts' not in names:
            self.tree_nut_type = False

    # Define the locked fields after product creation
    _LOCKED_FIELDS = [
        'type',  # Product Type
        'product_category_type',  # Product Category Type (your custom field)
        'auto_sequence_code',  # Auto Sequence Code
        'barcode',  # Bar Code
    ]

    def write(self, vals):
        if any(field in vals for field in self._LOCKED_FIELDS):
            locked_attempts = [f for f in self._LOCKED_FIELDS if f in vals]
            for record in self:
                if record.id:  # only block updates on existing records
                    raise ValidationError(_(
                        "The following fields cannot be changed after the product is created: %s"
                    ) % ', '.join(locked_attempts))

        # ✅ call Odoo's parent class, not yourself
        return super().write(vals)

    # def write(self, vals):
    #     if any(field in vals for field in self._LOCKED_AFTER_CREATE):
    #         locked_fields_attempt = [f for f in self._LOCKED_AFTER_CREATE if f in vals]
    #         if self.filtered(lambda r: r.id):
    #             raise ValidationError(_(
    #                 "The following fields cannot be changed after creation: %s"
    #             ) % (', '.join(locked_fields_attempt)))
    #     return super(ProductTemplate, self).write(vals)

    # @api.model
    # def create(self, vals):
    #     code = vals.get('auto_sequence_code')
    #     if code and len(str(code)) > 4:
    #         raise ValidationError(_("Auto Sequence Code must be 4 characters max."))
    #     return super(ProductTemplate, self).create(vals)



# -*- coding: utf-8 -*-
from odoo import models, fields,api
from odoo.exceptions import ValidationError


BOX_TYPE_SELECTION = [
    ('retail_box', 'Retail Box 9 7/8 x 9 7/8 x 6 1/8 (2/5 LB)'),
    ('fsh_box', 'FSH Box 12 5/8 x 10 7/16 x 6 5/8 (2/10 LB & 2 Trays)'),
    ('clamshell_full', 'Full Size Clamshell 19 3/8 x 11 1/2 x 5 7/8 (24/12 oz & 16/16 oz)'),
    ('12_layer_patty', '12 Layer Patty Box 17 1/4 x 13 1/4 x 5 1/4 (120)'),
]

NET_WEIGHT_UOM = [
    ('oz', 'OZ'),
    ('lb', 'LB'),
]

PACK_UOM_SELECTION = [
    ('oz','OZ'), ('lb','LB'), ('gal','GAL'), ('ea','EA'),
    ('pk','PK'), ('l','L'), ('ct','CT')
]

PACK_CONTAINER_SELECTION = [
    ('cs','CS'), ('pail','Pail'), ('bags','Bags')
]

BASIC_PREP_OPTIONS = [
    ('best_before', 'Best Before Date'),
    ('expiration', 'Expiration Date'),
    ('packaging', 'Packaging Date'),
    ('production', 'Production Date'),
    ('use_by', 'Use By Date'),
]

INVENTORY_LOCATIONS = [
    ('finished_cooler_1','Finished Goods Cooler 1'),
    ('finished_cooler_2','Finished Goods Cooler 2'),
    ('raw_material_cooler_3','Raw Material Cooler 3'),
    ('freezer_1','Freezer 1'),
    ('red_meat_1','Red Meat 1'),
    ('poultry_1','Poultry 1'),
    ('dry_goods_1','Dry Goods 1'),
    ('chemical_station_1','Chemical Station 1'),
    ('tool_station_1','Tool Station 1'),
    ('shipping_station_1','Shipping Station 1'),
    ('front_office_1','Front Office 1'),
    ('stock_room_1','Stock Room 1'),
    ('employee_room_1','Employee Room 1'),
    ('main_floor','Main Floor'),
    ('semi_finished_goods_1','Semi-Finished Goods Location 1'),
]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    type = fields.Selection(
        string="Product Type",
        help="Goods are tangible materials and merchandise you provide.\n"
             "A service is a non-material product you provide.",
        selection=[
            ('consu', "Goods"),
            ('service', "Service"),
        ],
        required=True,
        default='consu',
    )

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





    # GENERAL
    description = fields.Text(string='Description')
    # renaming only in view; keep category fields intact. If using product.public.category, we can change label in view.
    tag_ids = fields.Text(string='Description')
    # tag_ids = fields.Many2many(
    #     'product.tag', 'product_template_tag_rel', 'prod_tmpl_id', 'tag_id',
    #     string='Tags'
    # )
    information_owner_gln = fields.Char(string='Information Owner GLN', size=15,
                                        help='15 numeric chars (GLN)')
    ingredients = fields.Text(string='Ingredients', size=1100)
    contains = fields.Char(string='Contains', size=200)
    allergen_statement_text = fields.Char(string='Allergen Statement', size=200)
    shelf_life_days = fields.Integer(string='Shelf Life (Days)',
                                     help='Enter number of days (max 3 digits)')

    # Attachments handled via generic relation (one2many to ir.attachment)
    attachment_ids = fields.One2many('ir.attachment', 'res_id',
                                     domain=[('res_model','=','product.template')],
                                     string='Attachments')

    # MARKETING
    brand_name = fields.Char(string='Brand Name')
    marketing_message = fields.Text(string='Marketing Message', size=1000)
    basic_preparation = fields.Selection(BASIC_PREP_OPTIONS, string='Basic Preparation')
    serving_information = fields.Text(string='Serving Information', size=1000)

    # INVENTORY / PACKAGING
    inventory_location = fields.Selection(INVENTORY_LOCATIONS, string='Inventory Location')

    # Pack size: 2 numbers, UOM and container type. Example: 2 / 10 LB Bags
    pack_size_qty_1 = fields.Integer(string='Pack Size Qty 1')
    pack_size_qty_2 = fields.Integer(string='Pack Size Qty 2')
    pack_size_uom = fields.Selection(PACK_UOM_SELECTION, string='Pack Size UoM')
    pack_container_type = fields.Selection(PACK_CONTAINER_SELECTION, string='Pack Container Type')

    net_weight = fields.Float(string='Net Weight')
    net_weight_uom = fields.Selection(NET_WEIGHT_UOM, string='Net Weight UoM',
                                     help='Net weight excludes packaging')

    box_type = fields.Selection(BOX_TYPE_SELECTION, string='Box Type')

    # Dimensions (all numeric; units IN for dims, weight unit same as net_weight_uom)
    package_height_in = fields.Float(string='Package Height (IN)')
    package_depth_in = fields.Float(string='Package Depth (IN)')
    package_width_in = fields.Float(string='Package Width (IN)')
    package_weight = fields.Float(string='Package Weight (gross)')
    package_weight_uom = fields.Selection(NET_WEIGHT_UOM, string='Package Weight UoM')

    layers_per_pallet = fields.Integer(string='Layers Per Pallet')
    items_per_layer = fields.Integer(string='Items Per Layer')
    pallet_height_in = fields.Float(string='Pallet Height (IN)')

    # Optional helper computed field to show Pack Size summary
    pack_size_display = fields.Char(string='Pack Size Display', compute='_compute_pack_display')

    @api.depends('pack_size_qty_1','pack_size_qty_2','pack_size_uom','pack_container_type')
    def _compute_pack_display(self):
        for rec in self:
            parts = []
            if rec.pack_size_qty_1:
                parts.append(str(rec.pack_size_qty_1))
            if rec.pack_size_qty_2:
                parts.append(str(rec.pack_size_qty_2))
            if rec.pack_size_uom:
                parts.append(rec.pack_size_uom.upper())
            if rec.pack_container_type:
                parts.append(rec.pack_container_type.upper())
            rec.pack_size_display = ' / '.join(parts) if parts else False

    @api.constrains('information_owner_gln')
    def _check_gln(self):
        for rec in self:
            if rec.information_owner_gln and len(rec.information_owner_gln) != 15:
                raise ValidationError("Information Owner GLN must be exactly 15 characters.")

    @api.constrains('shelf_life_days')
    def _check_shelf_life(self):
        for rec in self:
            if rec.shelf_life_days and (rec.shelf_life_days < 0 or rec.shelf_life_days > 999):
                raise ValidationError("Shelf life must be 0-999 days.")

    @api.onchange("product_category_type")
    def _onchange_product_category_type(self):
        if self.product_category_type:
            prefix = self.product_category_type.name.strip().upper()  # e.g. FG

            # find last product with same category type
            last = self.env["product.template"].search(
                [("product_category_type", "=", self.product_category_type.id),
                 ("auto_code", "like", f"{prefix}%")],
                order="auto_code desc",
                limit=1
            )

            if last and last.auto_code and last.auto_code.startswith(prefix):
                try:
                    last_number = int(last.auto_code.replace(prefix, "") or 0)
                except ValueError:
                    last_number = 0
            else:
                last_number = 0

            new_number = last_number + 1
            self.auto_code = f"{prefix}{str(new_number).zfill(4)}"  # e.g. FG0001
        else:
            self.auto_code = False

