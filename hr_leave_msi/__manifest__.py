# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'HR Leave',
    'author': 'MSI',

    'description': """
    """,
    'summary': 'Leave Management',

    'sequence': 33,
    'images': [''],
    'depends': [
        'base',
        'hr',
        'hr_management_time',
    ],
    'data': [
        'data/product_data.xml',
        'data/sequence.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/seting.xml',
        'views/leave_allocation.xml',
        'views/uang_cuti.xml',
    ],
    "application": True,

}
