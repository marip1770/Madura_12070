# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2018 Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

{
    'name': "Print Overtime",
    'author': 'MSI',
    'category': 'Print',
    'description': """ Print Payroll
              1. Created on April 20 2020
""",
    'version': '1.0.0',
    'depends': ['base',
        'msi_hr_payroll',],
    'data': [
        'report/print_surat_templates.xml',
        'report/print_surat.xml',
#        'views/msi_print_internal.xml'

],
    'installable': True,
    'application': True,
    'auto_install': False,
}
