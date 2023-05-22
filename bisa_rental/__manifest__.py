# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Operational Rental Management',
    'author': 'BISA',

    'description': """
    """,
    'summary': 'Management Operational Rental Management',

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
        'views/rental.xml',

    ],
    "application": True,

}
