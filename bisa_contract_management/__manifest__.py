# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Operational Contract Management',
    'author': 'BISA',

    'description': """
    """,
    'summary': 'Management Operational Contract Management',

    'sequence': 32,
    'images': [''],
    'depends': [
        'base',
        'hr',
        'uom',
        'product',
        'project',
        'sale',
        'bisa_hauling',
    ],
    'data': [
        'data/data.xml',
        'data/sequence.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/contract_management.xml',

    ],
    "application": True,

}
