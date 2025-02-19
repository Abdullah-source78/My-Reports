#-*- coding:utf-8 -*-


from odoo import api, models, fields
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import Warning
import datetime
from datetime import date
from datetime import date, timedelta
import datetime
from dateutil.relativedelta import *
import math
from PIL import Image, ImageDraw
import time
from datetime import datetime as dt
from datetime import date, datetime, timedelta
import re
import pandas as pd
import numpy as np
import psycopg2 as pg
import pandas.io.sql as psql
import getpass
from operator import itemgetter
from itertools import groupby

class ProductMovementClass(models.AbstractModel):
    _name = 'report.product_movement_report.product_movement_report'
    _description = 'Product Movement Report'


   

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        

        form = docs.form
        to = docs.to
        typee = docs.typee
        product_ids = docs.product_id


        # domain = [('date', '>=', form), ('date', '<=', to)]

        # if typee == 'specific' and product_ids:
        #     stock_transfer_lines = self.env['stock.transfer.line'].search([
        #         ('product_id', 'in', product_ids.ids)
        #     ])
        #     transfer_ids = stock_transfer_lines.mapped('stock_transfer_id').ids  



        #     if transfer_ids:
        #         domain.append(('id', 'in', transfer_ids))
        #         domain.append(('stock_transfer_line_ids.product_id', 'in', product_ids.ids))
        #     else:
        #         domain.append(('id', '=', 0))


        # print("Domain being used:", domain)


        
        domain = [('stock_transfer_line_ids.product_id', 'in', product_ids.ids)]
        
        receipts = self.env['stock.transfer'].search(domain + [('delivery_type', '=', 'receipts'),('date', '>=', form), ('date', '<=', to)])
        deliveries = self.env['stock.transfer'].search(domain +[('delivery_type', '=', 'deliveries'),('date', '>=', form), ('date', '<=', to)])


        
        
  
        data_list = []

        
        for rec in receipts:
            for move in rec.stock_transfer_line_ids:  
                if move.product_id in product_ids:  
                    data_list.append({
                        'product_name': move.product_id.name,
                        'date': rec.date,
                        'source_location': rec.project_id.name,
                        'destination_location': rec.po_ref_id.delivery_location_id.name,
                        'picking_ref': rec.po_ref_id.name,
                        'party': rec.vendor_id.name if rec.vendor_id else '',
                        'price': move.product_id.list_price,
                        'quantity_in': move.to_do_qty,
                        'quantity_out': 0.0,
                    })


        
        for rec in deliveries:
            for move in rec.stock_transfer_line_ids:  
                if move.product_id in product_ids:  
                    data_list.append({
                        'product_name': move.product_id.name,
                        'date': rec.date,
                        'source_location': rec.receive_location_id.name,
                        'destination_location': rec.delivery_location_id.name,
                        'picking_ref': rec.so_ref_id.reference,
                        'party': rec.vendor_id.name if rec.vendor_id else '',
                        'price': move.product_id.list_price,
                        'quantity_in': 0.0, 
                        'quantity_out': move.to_do_qty,
                    })




    # Create DataFrame for the results
        df = pd.DataFrame(data_list)

        if not df.empty:
            # Sort the DataFrame alphabetically by the 'product_name' column
            df = df.sort_values(by='product_name', ascending=True)
            data_list = df.to_dict(orient='records')

            # Group data by product name
            grouped_data = {}
            for product_name, group in groupby(data_list, key=lambda x: x['product_name']):
                grouped_data[product_name] = list(group)
        else:
            data_list = []  # Keep it empty for template check
            grouped_data = {}  # No grouped data if empty

        return {
            'doc_ids': docids,  
            'doc_model': model,
            'data': data,  
            'form': form, 
            'to': to,  
            'data_list': data_list,  # This will be empty if no data
            'grouped_data': grouped_data,  # Pass grouped data to template
            'no_data': len(data_list) == 0,  # Boolean flag for template
        }
