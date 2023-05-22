# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Users Addon',



    'summary': 'users Addon',

    'sequence': 32,
    'images': [''],
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/msi_users.xml',

    ],
    "application": True,

}
