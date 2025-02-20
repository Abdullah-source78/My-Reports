# -- coding: utf-8 --
{
    'name': "Bill Estimate Report",

    'summary': """Bill Estimate Report""",

    'description': """ Bill Estimate Report Working For POP""",
    'sequence': "1",
    'author': "wags.sa",
    'website': "https://wags.sa",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '16.5.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'product_serials_pop',
        'product_wags',
       
    ],

    # always loaded
    'data': [
        
        'security/ir.model.access.csv',
        'views/module_report.xml',
        # 'views/views.xml',
        # 'views/module_report.xml',
        'views/templates.xml',
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
