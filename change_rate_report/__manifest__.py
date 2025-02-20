# -- coding: utf-8 --
{
    'name': "Change Rate Report",

    'summary': """Change Rate Report""",

    'description': """ Change Rate Report Working For Toys""",
    'sequence': "-1000",
    'author': "wags.sa",
    'website': "https://wags.sa",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'change',
    'version': '16.5.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',  
    ],

    # always loaded
    'data': [
        
        'security/ir.model.access.csv',
        'views/module_report.xml',
        # 'views/views.xml',
        'views/module_report.xml',
        'views/templates.xml',
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
