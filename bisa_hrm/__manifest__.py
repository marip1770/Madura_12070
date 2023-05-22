# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Operational Road Maintenance',
    'author': 'BISA',

    'description': """
    """,
    'summary': 'Management Operational Road Maintenance',

    'sequence': 32,
    'images': [''],
    'depends': [
        'base',
        'hr',
        'uom',
        'product',
        'project',
    ],
    'data': [
        # 'data/product_data.xml',
        'data/sequence.xml',
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/hrm.xml',

    ],
    "application": True,

}
