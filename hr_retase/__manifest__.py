# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'HR Retase',
    'author': 'MSI',

    'description': """
    """,
    'summary': 'HR Retase',

    'sequence': 32,
    'images': [''],
    'depends': [
        'base',
        'hr',
        'hr_management_time',
    ],
    'data': [
        'data/product_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/retase.xml',
        'views/seting.xml',
        'views/proses_payroll.xml',
    ],
    "application": True,

}
