{
    'name': "Product Movement Report",

    'description': "Product Movement Report",
    'sequence':'-1000',

    'author': 'Peer Abdullah',
    
    'website': "http://www.ecube.pk",
    
    'category': 'invoice',
    
    'version': '14.0.01',
    'application': True,
    'depends': ['base','product' ],
    
    'data': [
        'template.xml',
        'views/module_report.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
}