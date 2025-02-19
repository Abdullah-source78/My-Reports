# #-*- coding:utf-8 -*-

import os
# import xlsxwriter
from datetime import date
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import datetime
import time
from odoo import api, models, fields
from odoo.exceptions import Warning,ValidationError
from odoo.tools import config
import base64
import string
import sys

class ProductMovementReport(models.TransientModel):
    _name = "product.movement.report"
    _description = 'Product Movement Report'


    to = fields.Date(string="to",default=date.today(),required=True)
    form = fields.Date(string="From", default=lambda self: date.today() - timedelta(days=60), required=True)
    typee = fields.Selection([("all" , "All"),("specific","Specific")],string = "Type",default="all")
    product_id = fields.Many2many('product.product',string ="Select Product" )

    
    def generate_report(self):
        
        data = {
            'form': self.read(['form', 'to', 'typee', 'product_id'])[0]
        }
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['form', 'to', 'typee', 'product_id'])[0])
        return self.env.ref('product_movement_report.report_for_product_movement_report').report_action(self, data=data)

