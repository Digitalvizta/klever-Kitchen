# -*- coding: utf-8 -*-

from odoo import models, fields, api
from math import ceil
import math


class MrpBom(models.Model):
    _inherit = 'mrp.bom'  # Inheriting the mrp.bom model

    batch_output = fields.Float(
        string="Batch Output",
        help="The batch output quantity",
        digits=(16, 1)  # Ensure it stores one decimal place
    )

    @api.model
    def create(self, vals):
        if 'batch_output' in vals:
            vals['batch_output'] = self._round_up(vals['batch_output'])

        return super(MrpBom, self).create(vals)

    def write(self, vals):
        if 'batch_output' in vals:
            vals['batch_output'] = self._round_up(vals['batch_output'])

        return super(MrpBom, self).write(vals)

    def _round_up(self, value):
        """Rounds up the value to 1 decimal place (e.g., 34.89 → 34.9)"""
        return math.ceil(value * 10) / 10.0



class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # Define batch_output field, but this will not be computed by default anymore
    batch_number = fields.Float(string="Batch Number")

    batch_output = fields.Float(
        string="Batch Output",
        help="The batch output quantity",
        digits=(16, 1)  # Ensure it stores one decimal place
    )

    @api.model
    def create(self, vals):
        if 'batch_output' in vals:
            vals['batch_output'] = self._round_up(vals['batch_output'])

        return super(MrpBom, self).create(vals)

    def write(self, vals):
        if 'batch_output' in vals:
            vals['batch_output'] = self._round_up(vals['batch_output'])

        return super(MrpBom, self).write(vals)

    def _round_up(self, value):
        """Rounds up the value to 1 decimal place (e.g., 34.89 → 34.9)"""
        return math.ceil(value * 10) / 10.0

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
        #     batch_output = self.product_qty / self.bom_id.batch_output
        #
        #     # Round up the batch_output to the nearest whole number using ceil (round up)
        #     self.batch_output = ceil(batch_output)
        #     values['batch_output'] = qty_produced / self.bom_id.batch_output



        # Call the parent write method to ensure all other logic is executed
        return super(MrpProduction, self).write(values)

    # def action_confirm(self):
    #     res = super().action_confirm()
    #     batch_output = self.product_qty / self.bom_id.batch_output
    #     self.batch_output = ceil(batch_output)
    #     return res

    def action_confirm(self):
        res = super().action_confirm()
        for record in self:
            if record.bom_id and record.bom_id.batch_output not in (0, None):
                batch_output = record.product_qty / record.bom_id.batch_output
                record.batch_output = ceil(batch_output)
            # else: silently skip or optionally log/debug
        return res

    @api.model
    def create(self, values):
        """
        Override the create method to ensure 'batch_output' and 'batch_number' are set
        based on 'product_qty' during record creation.
        """
        if 'product_qty' in values:
            bom_id = values['bom_id']
            bom = self.env['mrp.bom'].browse(bom_id)

            # Calculate batch_output by dividing product_qty by the bom's batch_output factor
            # values['batch_output'] = bom.product_qty / bom.batch_output
            if bom and bom.batch_output not in (0, None):
                # Safe division and rounding
                batch_output = values['product_qty'] / bom.batch_output
                values['batch_output'] = ceil(batch_output)

            # Round up the batch_output to the nearest whole number using ceil (round up)
            # values['batch_output'] = ceil(batch_output)

            # Update batch_number (assumed to be same as product_qty here)
            # values['batch_number'] = values.get('product_qty', 0)

        # Call the parent create method to create the record
        return super(MrpProduction, self).create(values)


