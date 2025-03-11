from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrderReportWizard(models.TransientModel):
    _name = 'wizard.report'
    _description = 'Sale Order Report Wizard'

    sale_order_id = fields.Many2one('sale.order', string="Sale Order")
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)

    def action_print_report(self):
        if not self.start_date or not self.end_date:
            raise UserError(_("Please select both Start Date and End Date."))

        if self.start_date > self.end_date:
            raise UserError(_("Start Date cannot be greater than End Date"))

        sale_orders = self.env['sale.order'].search([
            ('date_order', '>=', self.start_date),
            ('date_order', '<=', self.end_date),
        ])

        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'sale_order_ids': sale_orders.ids
        }

        return self.env.ref('print_sale_order_from_wizard.sale_order_report_print_from_wizard_action').report_action(self, data=data)
