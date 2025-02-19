from odoo import models, fields, api
import datetime

class BalanceSheetWizard(models.TransientModel):
    _name = "balance.sheet.wizard"
    _description = "Balance Sheet Wizard"

    date_from = fields.Date(string="From Date", required=True, default=lambda self: datetime.date.today().replace(day=1))
    date_to = fields.Date(string="To Date", required=True, default=lambda self: datetime.date.today())

    def action_generate_balance_sheet(self):
        """Trigger report generation with selected date range"""
        return self.env.ref('custom_balance_sheet.report_for_custom_balance_sheet').report_action(self)
