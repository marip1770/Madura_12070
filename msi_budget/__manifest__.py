# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Budget & Cost Center',



    'summary': 'Budget & Cost Center',

    'sequence': 32,
    'images': [''],
    'depends': ['base','account_budget','purchase_request','purchase','account','msi_accounting','hr_expense','account_cost_center','msi_sales_quotations'],
    'data': [
        'security/ir.model.access.csv',
        'views/msi_budget.xml',
        'views/msi_cost_center.xml',
        'views/msi_purchase_request.xml',
        'views/msi_purchase_order.xml',
        'views/msi_account_invoice.xml',
        'views/msi_expense.xml',
        'views/msi_advance_settlement.xml',
        # 'wizard/transfer_budget.xml',

    ],
    "application": True,

}
