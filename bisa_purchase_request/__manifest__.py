{
    'name': 'Purchase request',
    'author': 'BISA',

    'description': """
    """,
    'summary': 'Purchase request',

    'sequence': 32,
    'images': [''],
    'depends': [
        'base',
        'hr',
        'uom',
        'product',
        'project',
        'purchase_request'
    ],
    'data': [
        'views/purchase_request.xml',
        'views/report_purchase_request.xml',
        'views/template_pr.xml'


    ],
    "application": True,

}