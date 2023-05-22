# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################
{
    'name': "Send Payslip by Email",
    'category': 'Payroll',
    'version': '1.0',
    'author': 'Equick ERP',
    'description': """
        This Module allows user to send mass mailing of Payslip.
        * Allow you to send email of Payslip to employee.
        * Allow you to send multiple employee payslip at same time.
        * You can send payslip email from Payslip Batches.
        * User can change the content of payslip email.
    """,
    'summary': """This Module allows user to send mass mailing of Payslip""",
    'depends': ['mail', 'hr_payroll'],
    'price': 12,
    'currency': 'EUR',
    'license': 'OPL-1',
    'website': "",
    'data': [
        'data/mail_data.xml',
        'views/payslip_view.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: