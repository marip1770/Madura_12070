# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'HR Payroll MSI',
    'author': 'MSI',
    'version' : '200904.a',
    'description': """
    """,
    'summary': 'Payroll Management',

    'sequence': 33,
    'images': [''],
    'depends': [
        'base',
        'hr',
        'msi_employee',
        'hr_contract',
        'account',
        'analytic',
    ],
    'data': [
        'data/product_data.xml',
        'report/print_surat_templates.xml',
        'report/print_surat.xml',
        'data/mail_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/structure.xml',
        'views/payroll.xml',
        'views/rekap_payroll.xml',
        'views/print_payroll.xml',
        'views/data.xml',
        'views/periode.xml',
    ],

    "application": True,

}
