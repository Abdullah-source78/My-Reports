



# -*- coding: utf-8 -*-
{
    'name': "Custom Balance Sheet",

    'summary': """ Custom Balance Sheet""",

    'description': """Custom Balance Sheet Working For Golden Saif""",
    'sequence': "-100",
    'author': "Peer Abdullah",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventry',
    'version': '15.5.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account',],  
    # 'css': ['static/src/css/report.css'],
    'data': [
        'security/ir.model.access.csv',
        'template.xml',
        'views/module_report.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

