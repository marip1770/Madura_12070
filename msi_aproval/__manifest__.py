# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Approval',
    'author': 'MSI',

    'description': """
     Approval\n
     - 4 Mar 2021 : Create by Ari\n
    """,
    'version' : '210304.1',
    'summary': 'Approval',
    'depends': ['mail','base','purchase_request','purchase','account','sale'],
    'sequence': 32,
    'data': [
        'data/data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        #'data/pemakaian_seq.xml',
        'views/menu_approval.xml',
        'views/sale_order.xml',
        'views/purchase_request.xml',
        'views/purchase_order.xml',
        'views/payment.xml',
        # 'views/advance.xml',

    ],
    "application": True,
}
