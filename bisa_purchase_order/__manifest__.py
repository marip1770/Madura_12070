{
    'name': 'Purchase order',
    'author': 'BISA',

    'description': """
    """,
    'summary': 'Purchase order',

    'sequence': 32,
    'images': [''],
    'depends': [
        'base',
        'hr',
        'uom',
        'product',
        'project',
        'purchase',
        
    ],
    'data': [
        'views/purchase_order.xml',
        'views/report_purchase_order.xml',
        'views/template_po.xml'


    ],
    "application": True,

}