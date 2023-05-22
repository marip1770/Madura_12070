# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Operational Plan Maintenance',
    'author': 'BISA',

    'description': """
    """,
    'summary': 'Management Operational  Plan Maintenance',

    'sequence': 32,
    'images': [''],
    'depends': [
        'base',
        'hr',
        'bisa_hauling',
        'product',
        'stock',
    ],
    'data': [
        'data/data.xml',
        # 'data/sequence.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/plan.xml',

    ],
    "application": True,

}
