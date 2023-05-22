# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'HR Peringatan dan Sanksi',
    'author': 'MSI',

    'description': """
    """,
    'summary': 'Peringatan, Sanksi',

    'sequence': 32,
    'images': [''],
    'depends': [
        'base',
        'hr',
    ],
    'data': [
        'data/product_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/sanksi.xml',

    ],
    "application": True,

}
