# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'HR Attendance Management',
    'author': 'MSI',
    'version' : '201128.4.0',
    'description': """
    """,
    'summary': 'Attendance Management',
    'sequence': 32,
    'images': [''],
    'depends': [
        'base',
        'msi_employee',
    ],
    'data': [
        'data/product_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/attendance.xml',
        'views/rekap_attendance.xml',
        'views/holiday.xml',
        'views/shift.xml',
        'views/jam_kerja.xml',
#        'views/hari_kerja.xml',
        'views/employee_group.xml',
        'views/form_request.xml',
        'views/periode.xml',
        'views/gen_schedule.xml',
    ],
    "application": True,

}
