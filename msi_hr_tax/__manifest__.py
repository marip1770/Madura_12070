# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'HR Tax',
    'author': 'MSI',

    'description': """
    """,
    'summary': 'Payroll Tax Management',

    'sequence': 33,
    'images': [''],
    'depends': [
        'base',
        'msi_employee',
    ],
    'data': [
        'data/product_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/structure.xml',
        'views/input_payroll.xml',
        'views/proses_tax.xml',
    ],
    "application": True,

}
