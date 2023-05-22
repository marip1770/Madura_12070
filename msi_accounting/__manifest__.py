# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'BISA Accounting',



    'summary': 'Accounting',

    'sequence': 32,
    'images': [''],
    'depends': ['base',
                # 'msi_terbilang',
                'account',
                'account_cancel',
                'account_asset',
                'account_accountant',
                'purchase',
                'purchase_request',
                'hr_expense',
              ],
    'data': [
        'data/sequence.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/msi_asset.xml',
        # 'views/invoice.xml',
        # 'views/expense.xml',
        # 'views/msi_account_move.xml',
        # 'views/lock_date.xml',
    ],
    "application": True,

}
