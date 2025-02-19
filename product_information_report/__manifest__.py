# -*- coding: utf-8 -*-
{
	'name': "Product Information Report",

	'summary': """ Product Information Report Working For Toys""",

	'description': """ Product Information Report Working For Toys""",
	'sequence': "1",
	'author': "wags.sa",
	'website': "https://wags.sa",

	# Categories can be used to filter modules in modules listing
	# Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
	# for the full list
	'category': 'Sale',
	'version': '16.5.1',

	# any module necessary for this one to work correctly
	'depends': ['base','product_wags'],  
	'css': ['static/src/css/report.css'],
	'data': [
	    'security/ir.model.access.csv',
        'template.xml',
    ],
	'installable': True,
	'application': True,
	'auto_install': False,
	'license': 'LGPL-3',
}