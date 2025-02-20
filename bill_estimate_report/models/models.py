from odoo import models, fields, api
from num2words import num2words  
from datetime import datetime

class BillEstimateReport(models.AbstractModel):
	_name = 'report.bill_estimate_report.bill_estimate_xml'
	_description = 'Bill Estimate Report'



	def calculate_date(self):
		date_str = "2024-09-18"

		parsed_date = datetime.strptime(date_str, '%Y-%m-%d')

		formatted_date = parsed_date.strftime('%b %d, %Y')
		return formatted_date

	@api.model
	def _get_report_values(self, docids, data=None):
		records = self.env['account.invoice.wags'].browse(docids)
		company = self.env['res.company'].search([], limit=1)  

		def get_name():
			value = " "
			if records.type == "out_invoice":
				value = "Customer Invoice"
			elif records.type == "in_invoice":
				value = "Supplier Invoice"
			return value

		def get_stage(state):
			stages = {
				"draft": "Draft",
				"cancel": "Cancelled",
				"open": "Posted",
				"refund": "Refund",
				"paid": "Paid",
			}
			return stages.get(state, "Unknown")

		def get_water_stage(state):
			stages = {
				"draft": "Draft",
				"cancel": "Cancel",
			}
			return stages.get(state, "Unknown")

		

		def number_to_spell(attr):
			word = num2words(attr)
			currency_names = {
				'USD': "US Dollar",
				'CNY': "Chinese Yuan",
				'EUR': "Euro",
				'GBP': "Pound",
				'JPY': "Japanese YEN",
				'PKR': "PKR"
			}
			currency_name = currency_names.get(records.partner_id.currency_id.name, "")
			return f"{currency_name} {word.title()} Only" if currency_name else f"{word.title()} Only"

		def get_state(attr):
			return attr.upper()

		users = self.env['res.users'].search([('id', '=', self.env.uid)], limit=1)

		barcodes = self.env['sale.serial.line'].search([('sale_id', '=', records.so_ref_id.id)])

		docargs = {
			'doc_ids': docids,
			'doc_model': 'account.invoice.wags',
			'docs': records,
			'get_name': get_name,
			'get_stage': get_stage,
			'get_water_stage': get_water_stage,
			'company': company,
			'get_state': get_state,
			'users': users,
			'number_to_spell': number_to_spell,
			'barcodes': barcodes,
		}
		print(docargs)

		return docargs





