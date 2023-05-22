# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'HR Promosi Mutasi',
    'author': 'MSI',

    'description': """
    """,
    'summary': 'Promosi Mutasi',

    'sequence': 32,
    'images': [''],
    'depends': [
        'base',
        'hr',
        'msi_employee',
        'msi_print_payroll',
    ],
    'data': [
        'data/product_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/mutasi.xml',

    ],
    "application": True,

}
