ok# -*- coding: utf-8 -*-

from odoo import models, fields, api
from math import ceil


class MrpBom(models.Model):
    _inherit = 'mrp.bom'  # Inheriting the mrp.bom model

    # Add the new batch_output field
    batch_output = fields.Float(string="Batch Output", help="The batch output quantity")


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # Define batch_output field, but this will not be computed by default anymore
    batch_output = fields.Float(string="Batch Output")
    batch_number = fields.Float(string="Batch Number")

    batch_function = fields.Char(string="Function")
    # Many2one field to link with mrp.workcenter
    workcenter_id = fields.Many2one('mrp.workcenter', string="Work Center")
    operation_id = fields.Many2one('mrp.routing.workcenter', string="Operation")

    def write(self, values):
        """
        Override the write method to customize the update of 'batch_output' and 'batch_number'
        when 'product_qty' is updated.
        """
        # If product_qty is being updated, calculate batch_output and batch_number
        if 'product_qty' in values:
            # Update batch_output by dividing product_qty by 270
            # values['batch_output'] = values['product_qty'] / 270
            batch_output = values['product_qty'] / self.bom_id.batch_output

            # Round up the batch_output to the nearest whole number using ceil (round up)
            values['batch_output'] = ceil(batch_output)

            # Update batch_number (you can modify this logic as needed)
            values['batch_number'] = values.get('product_qty', 0)  # Use product_qty or default to 0 if missing
        # else:
        #     values['batch_output'] = qty_produced / self.bom_id.batch_output



        # Call the parent write method to ensure all other logic is executed
        return super(MrpProduction, self).write(values)

    @api.model
    def create(self, values):
        """
        Override the create method to ensure 'batch_output' and 'batch_number' are set
        based on 'product_qty' during record creation.
        """
        if 'product_qty' in values:
            bom_id  = values['bom_id']
            bom = self.env['mrp.bom'].browse(bom_id)

            # Calculate batch_output by dividing product_qty by the bom's batch_output factor
            batch_output = values['product_qty'] / bom.batch_output

            # Round up the batch_output to the nearest whole number using ceil (round up)
            values['batch_output'] = ceil(batch_output)

            # Update batch_number (assumed to be same as product_qty here)
            values['batch_number'] = values.get('product_qty', 0)

        # Call the parent create method to create the record
        return super(MrpProduction, self).create(values)


