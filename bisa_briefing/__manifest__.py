# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Operational Briefing',
    'author': 'BISA',

    'description': """
    """,
    'summary': 'Management Operational Briefing',

    'sequence': 32,
    'images': [''],
    'depends': [
        'base',
        'hr',
    ],
    'data': [
        # 'data/product_data.xml',
        # 'data/sequence.xml',
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/briefing.xml',

    ],
    "application": True,

}
