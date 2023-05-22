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

class tbl_msi_overtime(models.Model):
    _name = 'tbl_msi_overtime'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sc_date_start desc'

    name = fields.Char('Nomor', default='New', readonly=True)
    date = fields.Date('Date', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    sc_date = fields.Date('Schedule Date', compute='_compute_tgl', store=True)  
    sc_date_start = fields.Datetime('Schedule Date start', required=True)  
    sc_date_end = fields.Datetime('Schedule Date end', required=True)
    description = fields.Char('Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve1', 'Approved1'),
        ('approve2', 'Approved2'),
        ('done', 'Done'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    detail = fields.One2many('tbl_msi_rekap_overtime','details','Detail')
    is_bill_to = fields.Boolean('Bill to')
    partner_id = fields.Many2one('res.partner','Partner')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('lembur') or _('New')#

        result = super(tbl_msi_overtime, self).create(vals)
        return result

    @api.one
    @api.depends('sc_date_start')
    def _compute_tgl(self):
    	if self.sc_date_start:
            tanggal = self.sc_date_start.strftime("%Y-%m-%d")
            self.sc_date = tanggal

    @api.one
    def action_submit(self):
        self.state = 'submit'
        for emp in self.detail:
            dur = self.sc_date_end - self.sc_date_start
            emp.durasi = dur.total_seconds()/3600

    @api.one
    def action_approve1(self):
        self.state = 'approve1'

    @api.one
    def action_ulang(self):
        self.state = 'submit'

 
    @api.one
    def action_approve2(self):
        self.state = 'approve2'
        for emp in self.detail:
            cari2 = self.env['tbl_msi_rekap_attendance'].search(
                       [('employee', '=', emp.employee.id),
                       ('sc_date_a', '=', self.sc_date)], limit=1)
            if cari2:
                      cari2.lembur_spkl_start = self.sc_date_start
                      cari2.lembur_spkl_end = self.sc_date_end
                      cari2.lembur_spkl = emp.durasi
                      cari2.parameter_ch = fields.Datetime.now()
            else:
                      raise UserError(_('Employee "%s" Tidak ada daam rekap' % (emp.employee.name, )))


    @api.one
    def action_done(self):
        self.state = 'done'

class tbl_msi_rekap_overtime(models.Model):
    _name = 'tbl_msi_rekap_overtime'
    _order = 'date desc'


    details = fields.Many2one('tbl_msi_overtime','Detail')
    nomor = fields.Char('Nomor', readonly=True, related='details.name', store=True)
    date = fields.Date('Date', readonly=True, related='details.date', store=True)
    sc_date = fields.Date('Schedule Date', readonly=True, related='details.sc_date', store=True)  
    sc_date_start = fields.Datetime('Schedule Date start', readonly=True, related='details.sc_date_start', store=True)  
    sc_date_end = fields.Datetime('Schedule Date end', readonly=True, related='details.sc_date_end', store=True)
    act_date_start = fields.Datetime('Actual Date start')  
    act_date_end = fields.Datetime('Actual Date end')
    name = fields.Char('NIK')
    employee = fields.Many2one('hr.employee','Employee')
    department_id = fields.Many2one('hr.department', 'Department', related='employee.department_id', store=True)
    description = fields.Char('Description', readonly=True, related='details.description', store=True)
    durasi = fields.Float('Durasi')
    value = fields.Float('Value')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ('done', 'Done'),
        ], string='Status', related='details.state', store=True)

    user = fields.Many2one('res.users','User', readonly=True, related='details.user')
    is_bill_to = fields.Boolean('Bill to', related='details.is_bill_to', store=True)
    partner_id = fields.Many2one('res.partner','Partner', related='details.partner_id', store=True)

    @api.onchange('employee')
    def _compute_employee(self):
        if self.employee:
            self.name = self.employee.nik



class tbl_msi_overtime_billing(models.Model):
    _name = 'tbl_msi_overtime_billing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char('Nomor', default='New', readonly=True)
    date = fields.Date('Date', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    periode = fields.Many2one('tbl_msi_periode_bulan','Period',required=True)
    department_id = fields.Many2one('hr.department', 'Department',required=True)
    partner_id = fields.Many2one('res.partner','Bill to',required=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ('create_bill', 'Create Bill'),
        ('done', 'Done'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    detail = fields.One2many('tbl_msi_rekap_overtime_billing','details','Detail')

    total_value = fields.Float(compute='_compute_total_value', string='Total Value', readonly=True, store=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('lembur_biling') or _('New')#

        result = super(tbl_msi_overtime_billing, self).create(vals)
        return result

    def act_get_data(self):
        detail_obj = self.env['tbl_msi_rekap_overtime_billing']
      
        if self.detail:
           self.detail.unlink()

        cari = self.env['tbl_msi_rekap_overtime'].search(
                       [('id', '>', 0)])
        for rekap in cari:
            cari2 = self.env['tbl_msi_rekap_attendance'].search(
                       [('employee', '=', rekap.employee.id),
                       ('sc_date_a', '=', rekap.sc_date)], limit=1)
            if cari2:
                rekap.act_date_start = cari2.act_date_in
                rekap.act_date_end = cari2.act_date_out

        self.env.cr.execute('SELECT name, employee, sc_date_start, sc_date_end, value FROM tbl_msi_rekap_overtime\
                             WHERE department_id = %s and partner_id = %s and act_date_start >= %s and act_date_start <= %s and is_bill_to = %s and state = %s' ,(self.department_id.id, self.partner_id.id, self.periode.date_awal, self.periode.date_akhir, True, 'done'))

        for row in self.env.cr.fetchall():

                 data_line2 = detail_obj.create({
                    'details': self.id,
                    'name': row[0],
                    'employee': row[1],
                    'periode': self.periode.id,
                    'lembur_spkl_start': row[2],
                    'lembur_spkl_end': row[3],
                    # 'akt_lembur_spkl': row[5],
                    'lembur_value': row[4],
                 })

    # def act_get_data(self):
    #     detail_obj = self.env['tbl_msi_rekap_overtime_billing']


    # def action_done(self):
#        self.state = 'done'


    @api.multi
    @api.depends('detail')
    def _compute_total_value(self):
        for wo in self:
            for harga in wo.detail:        
               wo.total_value += harga.lembur_value

class tbl_msi_rekap_overtime_billing(models.Model):
    _name = 'tbl_msi_rekap_overtime_billing'
    _order = 'date desc'


    details = fields.Many2one('tbl_msi_overtime_billing','Detail')
    nomor = fields.Char('Nomor', readonly=True, related='details.name')
    date = fields.Date('Date', readonly=True, related='details.date')
    periode = fields.Many2one('tbl_msi_periode_bulan','Period', readonly=True)
    lembur_spkl_start = fields.Datetime('Jad SPKL Msk', readonly=True)
    lembur_spkl_end = fields.Datetime('Jad SPKL Plg', readonly=True)
    name = fields.Char('NIK', readonly=True)
    employee = fields.Many2one('hr.employee','Employee', readonly=True)
    department_id = fields.Many2one('hr.department', 'Department', related='employee.department_id', store=True)
    akt_lembur_spkl = fields.Float('Akt SPKL (Jam)', help='Durasi Lembur SPKL dalam jam', readonly=True)
    lembur_value = fields.Float('Lembur (Value)', help='Durasi Lembur dalam Rp')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ('create_bill', 'Create Bill'),
        ('done', 'Done'),
        ], string='Status', readonly=True, related='details.state')
    user = fields.Many2one('res.users','User', readonly=True, related='details.user')


    @api.onchange('employee')
    def _compute_employee(self):
        if self.employee:
            self.name = self.employee.nik

