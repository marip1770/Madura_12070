# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'MSI Budget Report',



    'summary': 'Budget Report',

    'sequence': 32,
    'images': [''],
    'depends': ['base',
                'account',
                'account_budget',
                'account_asset',
                'account_accountant',
              ],
    'data': [
        'security/ir.model.access.csv',
        'views/msi_budget.xml',
    ],
    "application": True,

}
