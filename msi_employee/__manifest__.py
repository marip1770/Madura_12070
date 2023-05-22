# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Employee Addon',



    'summary': 'Human Resources',

    'sequence': 32,
    'images': [''],
    'depends': [
        'hr',
        'base',
        'project',
    ],
    'data': [
        'data/nik.xml',
        'security/ir.model.access.csv',
        'views/msi_employee.xml',
        'views/seting.xml',

    ],
    "application": True,

}

