# #-*- coding:utf-8 -*-
# ##############################################################################
# #
# #    OpenERP, Open Source Management Solution
# #    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
# #
# #    This program is free software: you can redistribute it and/or modify
# #    it under the terms of the GNU Affero General Public License as published by
# #    the Free Software Foundation, either version 3 of the License, or
# #    (at your option) any later version.
# #
# #    This program is distributed in the hope that it will be useful,
# #    but WITHOUT ANY WARRANTY; without even the implied warranty of
# #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# #    GNU Affero General Public License for more details.
# #
# #    You should have received a copy of the GNU Affero General Public License
# #    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# #
# ##############################################################################
from odoo import models, fields, api
from datetime import date

class ProductInformationReportTreeview(models.TransientModel):
    _name = "product.information.report"

    form = fields.Date(string="From", default=date.today())
    to = fields.Date(string="To", default=date.today())

    @api.model
    def view(self, context=None):

        product_information = self.env['product.information.treeview']

        self._cr.execute("DELETE FROM product_information_treeview")
        
        query = """
            INSERT INTO product_information_treeview
            (sr_no, product_id, product_code, item_number, other_number, brand_id, barcode_1, base_price, khi_wh_stock, isd_wh_stock, lhr_wh_stock,isb_disp,lhr_disp,khi_disp)
            SELECT
                ROW_NUMBER() OVER() AS sr_no,
                pp.id AS product_id,
                pp.default_code AS product_code,
                pp.item_id AS item_number,
                pp.alternate_no AS other_number,
                pp.brand_id AS brand_id,
                pp.barcode AS barcode_1,
                pp.list_price AS base_price,
                COALESCE(SUM(CASE WHEN pq.location_id = 7 THEN pq.quantity ELSE 0 END), 0) AS khi_wh_stock,
                COALESCE(SUM(CASE WHEN pq.location_id = 6 THEN pq.quantity ELSE 0 END), 0) AS isd_wh_stock,
                COALESCE(SUM(CASE WHEN pq.location_id = 5 THEN pq.quantity ELSE 0 END), 0) AS lhr_wh_stock,
                COALESCE(SUM(CASE WHEN pq.location_id = 8 THEN pq.quantity ELSE 0 END), 0) AS isb_disp,
                COALESCE(SUM(CASE WHEN pq.location_id = 30 THEN pq.quantity ELSE 0 END), 0) AS lhr_disp,
                COALESCE(SUM(CASE WHEN pq.location_id = 31 THEN pq.quantity ELSE 0 END), 0) AS khi_disp
            FROM
                product_product_wags pp
            LEFT JOIN
                product_quantity_wags pq ON pq.product_id = pp.id
            WHERE
                pp.active = True
            GROUP BY
                pp.id, pp.default_code, pp.item_id, pp.alternate_no, pp.brand_id, pp.barcode, pp.list_price
            ORDER BY
                pp.id
        """
        self._cr.execute(query)

        return {
            'type': 'ir.actions.act_window',
            'name': "Product Information",
            'res_model': 'product.information.treeview',
            'view_type': 'form',
            'view_mode': 'tree,form,kanban,graph,pivot',
            'target': 'main',
            'context': {
                'search_default_group_description': 1,
            },
        }


class CustomerProductProfitReport(models.TransientModel):
    _name = "product.information.treeview"

    sr_no = fields.Integer(string="SR #")
    product_id = fields.Many2one('product.product.wags', string='Product Name')
    product_code = fields.Char(string="Product Code")
    item_number = fields.Char(string="Item Number")
    other_number = fields.Char(string="Alternative Number")
    brand_id = fields.Many2one('product.brand.wags', string='Brand Name')
    barcode_1 = fields.Char(string="Barcode 1")
    base_price = fields.Float(string="Base Price")
    khi_wh_stock = fields.Float(string="KHI-WH/Stock")
    isd_wh_stock = fields.Float(string="ISD-WH/Stock")
    lhr_wh_stock = fields.Float(string="LHR-WH/Stock")
    isb_disp = fields.Float(string="Islamabad DISP")
    lhr_disp = fields.Float(string="Lahore DISP")
    khi_disp = fields.Float(string="Karachi DISP")