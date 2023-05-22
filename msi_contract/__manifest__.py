# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'HR Contract Addon',



    'summary': 'Human Resources',

    'sequence': 32,
    'images': [''],
    'depends': [
        'hr',
        'base',
        'msi_employee',
        'hr_contract',
        'msi_hr_payroll',
    ],
    'data': [
#        'security/ir.model.access.csv',
        'views/contract.xml',
#        'views/seting.xml',

    ],
    "application": True,

}

