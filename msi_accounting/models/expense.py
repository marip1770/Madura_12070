# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import email_re, email_split, email_escape_char, float_is_zero, float_compare, \
    pycompat, date_utils
from odoo.exceptions import UserError, AccessError
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp

import math


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    code_transaksi = fields.Char('Code Transaksi',default='New', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('code_transaksi', _('New')) == _('New'):
                vals['code_transaksi'] = self.env['ir.sequence'].next_by_code('seq_cc') or _('New')

        sheet = super(HrExpenseSheet, self.with_context(mail_create_nosubscribe=True)).create(vals)
        sheet.activity_update()
        return sheet

class HrExpenseSheetRegisterPaymentWizard(models.TransientModel):

    _inherit = "hr.expense.sheet.register.payment.wizard"

    communication = fields.Char(string='Code Transaksi')
    communication1 = fields.Char(string='Memo')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        active_ids = self._context.get('active_ids', [])
        expense_sheet = self.env['hr.expense.sheet'].browse(active_ids)
        if expense_sheet.employee_id.id and expense_sheet.employee_id.sudo().bank_account_id.id:
            self.partner_bank_account_id = expense_sheet.employee_id.sudo().bank_account_id.id
            self.communication = expense_sheet.code_transaksi
        elif self.partner_id and len(self.partner_id.bank_ids) > 0:
            self.partner_bank_account_id = self.partner_id.bank_ids[0]
            self.communication = expense_sheet.code_transaksi
        else:
            self.partner_bank_account_id = False
            self.communication = expense_sheet.code_transaksi


    def _get_payment_vals(self):
        """ Hook for extension """
        return {
            'partner_type': 'supplier',
            'payment_type': 'outbound',
            'partner_id': self.partner_id.id,
            'partner_bank_account_id': self.partner_bank_account_id.id,
            'journal_id': self.journal_id.id,
            'company_id': self.company_id.id,
            'payment_method_id': self.payment_method_id.id,
            'amount': self.amount,
            'currency_id': self.currency_id.id,
            'payment_date': self.payment_date,
            'communication': self.communication,
            'communication1': self.communication1
        }