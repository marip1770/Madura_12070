# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare

class tbl_msi_print_payroll_batch(models.Model):
    _name = 'tbl_msi_print_payroll_batch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char('Name', compute="_compute_nama", store=True)
    periode = fields.Many2one('tbl_payroll_period','Period', required=True) 
    tipe = fields.Selection([
        ('regular', 'Regular'),
        ('adhoc', 'Adhoc'),
        ('exit', 'Exit'),
        ], string='Tipe', required=True, default='regular')
    date = fields.Date('Date', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    ket = fields.Char('Keterangan')  
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    detail = fields.One2many('tbl_msi_print_payroll_batch_line','details','Detail')
    detail_print = fields.One2many('tbl_msi_payroll_line','details_print','Detail Print')

    @api.one
    @api.depends('periode','ket', 'tipe')
    def _compute_nama(self):
        if self.periode and self.ket:
           self.name = 'PAYROLL ' + str(self.tipe).upper() + ' ' + str(self.periode.name).upper() + ' ' +str(self.ket).upper()

        if self.periode and not self.ket:
           self.name = 'PAYROLL ' + str(self.tipe).upper() + ' ' + str(self.periode.name).upper()

        if not self.periode and self.ket:
           self.name = 'PAYROLL ' + str(self.tipe).upper() + ' ' + str(self.ket).upper()

    @api.one
    def action_get(self):
        self.env.cr.execute('select id from tbl_msi_payroll_line where periode = %s and state = %s and tipe = %s', (self.periode.id, 'close', self.tipe))
        item2 = self.env.cr.fetchall()
        if item2:
           for r_item2 in item2:
               self.env.cr.execute("UPDATE tbl_msi_payroll_line set details_print = %s where id = %s",(self.id,r_item2[0]))



    @api.one
    def action_submit(self):
        self.state = 'submit'


    @api.one
    def action_sent12(self):
        for emp in self.detail:
            emp.name.action_payslip_sent()


    @api.multi
    def action_sent(self):
        compose_obj = self.env['mail.compose.message']
        all_fields = compose_obj._fields.keys()
        for payslip in self.detail_print:
            if payslip.employee.sent_email:
               compose_vals = payslip.action_payslip_sent()
               default_vals = compose_obj.with_context(compose_vals['context']).default_get(all_fields)
               compose_id = compose_obj.create(default_vals)
               compose_id.onchange_template_id_wrapper()
               compose_id.action_send_mail()




class tbl_msi_print_payroll_batch_line(models.Model):
    _name = 'tbl_msi_print_payroll_batch_line'
    _order = 'periode'


    details = fields.Many2one('tbl_msi_print_payroll_batch','Detail')
    employee = fields.Many2one('hr.employee','Employee')
    name = fields.Many2one('tbl_msi_payroll_line','NIK')
    tipe = fields.Selection([
        ('regular', 'Regular'),
        ('adhoc', 'Adhoc'),
        ('exit', 'Exit'),
        ], string='Tipe')
    periode = fields.Many2one('tbl_payroll_period','Period') 

    @api.onchange('name')
    def onchange_periode(self):
        if self.name:
            self.employee = self.name.employee.id
            self.periode = self.name.periode.id
            self.tipe = self.name.tipe







