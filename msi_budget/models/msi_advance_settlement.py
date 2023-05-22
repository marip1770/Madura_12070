# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from odoo import api, fields, models

import math

class tbl_msi_acc_settlement(models.Model):
    _inherit = 'tbl_msi_acc_settlement'


    def action_approve2(self):

      account_move_obj = self.env['account.move']
      account_move_line_obj = self.env['account.move.line']

      if not self.property_account_uang_muka:
         raise UserError(_('Account Advanced belum di set'))

      if not self.journal_id:
         raise UserError(_('Advanced Journal belum di set'))

      if not self.date_settlement:
         raise UserError(_('Tanggal Settlement belum di set'))



      data2 = account_move_obj.create({
                    'journal_id': self.journal_id.id,
                    'date': self.date_settlement,
                    'ref': 'Settlement # ' + str(self.name),

      })

      data4 = account_move_line_obj.with_context(check_move_validity=False).create({
                    'name': self.name,
                    'date': self.date_settlement,
                    'journal_id': self.journal_id.id,
                    'account_id': self.property_account_uang_muka.id,
                    'move_id': data2.id,
                    'date_maturity': fields.Date.today(),
                    'credit': self.settlement,

      })

          

      for line in self.detail_settlement_id:
          data3 = account_move_line_obj.with_context(check_move_validity=False).create({
                    'name': str(self.name) + ' ' + str(line.name),
                    'date': self.date_settlement,
                    'journal_id': self.journal_id.id,
                    'account_id': line.property_account_expense.id,
                    'analytic_account_id': line.analytic_id.id,
                    'cost_center_id': line.cost_center_id.id,
                    'move_id': data2.id,
                    'date_maturity': fields.Date.today(),
                    'debit': line.amount,
          })

      data2.post()



      if self.selisih < 0:

         detail_obj = self.env['account.payment']
         data_line2 = detail_obj.create({
            'payment_type': 'outbound',
            'partner_type': 'supplier',
            'partner_id': self.employee_id.address_home_id.id,
            'amount': self.selisih*-1,
            'journal_id': self.journal_id.id,
            'payment_method_id': 2,
            'communication': 'Settlement Lebih Advanced # ' + str(self.name) + ' ' +str(self.employee_id.name),
            'x_studio_field_cqQTC':'Settlement Lebih Advanced # ' + str(self.name) + ' ' +str(self.employee_id.name),
            'is_advance': True,
            'adv_account_id': self.property_account_uang_muka.id,
         })
         self.payment_inout_id = data_line2

      if self.selisih > 0:

         detail_obj = self.env['account.payment']
         data_line2 = detail_obj.create({
            'payment_type': 'inbound',
            'partner_type': 'supplier',
            'partner_id': self.employee_id.address_home_id.id,
            'amount': self.selisih,
            'journal_id': self.journal_id.id,
            'payment_method_id': 2,
            'communication': 'Settlement Advanced # ' + str(self.name) + ' ' +str(self.employee_id.name),
            'x_studio_field_cqQTC':'Settlement Advanced # ' + str(self.name) + ' ' +str(self.employee_id.name),
            'is_advance': True,
            'adv_account_id': self.property_account_uang_muka.id,
         })

         self.payment_inout_id = data_line2

      self.state = 'done'


class tbl_msi_acc_settlement_settlement(models.Model):
    _inherit = 'tbl_msi_acc_settlement_settlement'

    detail_settlement_ids = fields.Many2one('tbl_msi_acc_settlement','Detail')
    name = fields.Char('Label')
    amount = fields.Float('Amount') 
    property_account_expense = fields.Many2one('account.account', string="Expense Account", required=True)
    analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    cost_center_id = fields.Many2one(
        'account.cost.center',
        string='Cost Center',
        index=True)
