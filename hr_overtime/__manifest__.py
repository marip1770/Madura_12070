# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'HR Overtime',
    'author': 'MSI',

    'description': """
    """,
    'summary': 'Overtime Management',

    'sequence': 32,
    'images': [''],
    'depends': [
        'base',
        'hr',
        'hr_management_time',
    ],
    'data': [
        'data/product_data.xml',
        # 'report/print_surat_templates.xml',
        # 'report/print_surat.xml',
        # 'data/mail_data.xml',
        'data/sequence.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/overtime.xml',
    ],
    "application": True,

}
