# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Operational Hauling',
    'author': 'BISA',

    'description': """
    """,
    'summary': 'Management Operation Hauling',

    'sequence': 32,
    'images': [''],
    'depends': [
        'base',
        'account',
        'hr',
        'uom',
        'product',
        'project',
        'msi_employee',
    ],
    'data': [
        'data/data.xml',
        'data/sequence.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/invoice.xml',
        'views/menu.xml',
        # 'views/operasional.xml',
        'views/konsolidasi.xml',
        'views/hauling.xml',
        'views/hrm.xml',
        'views/rental.xml',
        'views/port.xml',
        'views/fuel_truck.xml',
        'views/water_truck.xml',
        'views/tls.xml',
        'views/user.xml',
        # 'views/pembuatan_billing.xml',
        # 'wizards/wizard_assigment.xml',

    ],
    "application": True,

}
