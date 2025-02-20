from odoo import models, fields, api
 
from datetime import datetime

class ChangeRateReport(models.AbstractModel):
	_name = 'report.change_rate_report.change_rate_xml'
	_description = 'Change Rate Report'

	@api.model
	def _get_report_values(self, docids, data=None):
		records = self.env['change.rate'].browse(docids)

		# listee = []
		# for rec in records:
		# 	for line in rec.product_rate_ids:
		# 		listee.append({
		# 			'order_from' : rec.order_from,
		# 			'date' : rec.date,
		# 			'product_id' : line.product_id,
		# 			'total_stock' : line.total_stock,
		# 			'cost_price' : line.cost_price,
		# 			'old_base_price' : line.old_base_price,
		# 			'new_base_price' : line.new_base_price,
		# 			'price_diff' : line.price_diff,
		# 			})



		docargs = {
			'doc_ids': docids,
			'doc_model': 'change.rate',
			'docs': records,
			# 'listee': listee,

		}
		print(docargs)

		return docargs





