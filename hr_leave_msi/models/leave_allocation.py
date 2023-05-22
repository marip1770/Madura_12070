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


class tbl_msi_leave_allocation_set(models.Model):
    _name = 'tbl_msi_leave_allocation_set'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

   
    name = fields.Char('Nomor', default='New', readonly=True)
    date = fields.Date('Date', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    periode_tahun = fields.Many2one('tbl_msi_periode_tahun','Period', required=True)
    alokasi_cuti = fields.Float('Alokasi Cuti', related='nama_group.alokasi', store=True)
    cuti_bersama = fields.Float('Cuti Bersama')
    cuti_tersedia = fields.Float('Cuti Tersedia', compute="_compute_cuti_tersedia", store=True)
    set_cuti = fields.Selection([
         ('employee','Per Employee'),
         ('group','Per Group'),
    ], string='Set Cuti', default='employee')
    nama_group = fields.Many2one('tbl_msi_leave_group','Nama Group')
    detail = fields.One2many('tbl_msi_leave_allocation','details','Detail Allocation')
    state = fields.Selection([
         ('draft','Draft'),
         ('submit','Submit'),
         ('done','Approved'),
         ('cancel','Canceled')
    ], string='State', default='draft', track_visibility='onchange')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('alokasi_cuti') or _('New')#

        result = super(tbl_msi_leave_allocation_set, self).create(vals)
        return result

    @api.one
    @api.depends('cuti_bersama','alokasi_cuti')
    def _compute_cuti_tersedia(self):
        self.cuti_tersedia = self.alokasi_cuti - self.cuti_bersama

    @api.onchange('periode_tahun')
    def _compute_periode_tahun(self):
    	if self.periode_tahun:
            self.env.cr.execute('select count(id) from tbl_msi_hari_libur where periode_tahun = %s and status = %s', (self.periode_tahun.id, 'CUTI_BERSAMA'))
            for hasil in self.env.cr.fetchall():
            #raise UserError(_(hasil[0]))
                self.cuti_bersama = hasil[0]


    @api.multi
    def action_get(self):
        alokasi_obj = self.env['tbl_msi_leave_allocation']
        if self.cuti_tersedia < 1:
            raise UserError(_("Cuti Tersedia tidak boleh kurang dari 1"))

        for nama in self.nama_group.detail:

              data31 = alokasi_obj.create({
                        'details': self.id,
                        'employee': nama.employee.id,
                        'periode_tahun': self.periode_tahun.id,
                        'alokasi_cuti': self.alokasi_cuti,
                        'cuti_bersama': self.cuti_bersama,
                        'is_active': True,
              })


class tbl_msi_leave_allocation(models.Model):
    _name = 'tbl_msi_leave_allocation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'periode_tahun desc, employee'


    details = fields.Many2one('tbl_msi_leave_allocation_set','Detail Allocation')
    date = fields.Date('Date', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    employee = fields.Many2one('hr.employee','Employee')
    nik = fields.Char('NIK', related='employee.nik', store=True)
    dept = fields.Many2one('hr.department', 'Department', related='employee.department_id', store=True)
    divisi = fields.Many2one('tbl_employee_divisi', 'Divisi', related='employee.divisi', store=True)
    loc = fields.Many2one('tbl_employee_lokasi', 'Lokasi', related='employee.lokasi', store=True)
    job = fields.Char('Job Title', related='employee.job_title', store=True)
    start_date = fields.Date('Start Working Date', related='employee.tgl_mulai', store=True)
    periode_tahun = fields.Many2one('tbl_msi_periode_tahun','Period', required=True)
    alokasi_cuti_sebelum = fields.Float('Previous Period')
    alokasi_cuti = fields.Float('Current Period')
    cuti_bersama = fields.Float('Holiday')
    cuti_terpakai = fields.Float('Leave Used', compute="_compute_cuti_terpakai", store=True)
    cuti_tersedia = fields.Float('Cuti Tersedia', compute="_compute_cuti_tersedia", store=True)
    name = fields.Char('Name', compute='_compute_nama', store=True, readonly=True)
    is_active = fields.Char('Active', default=True)
    state = fields.Selection([
         ('draft','Draft'),
         ('submit','Submit'),
         ('done','Approved'),
         ('cancel','Canceled')
    ], string='State', default='draft', track_visibility='onchange', related='details.state', store=True)
    detail = fields.One2many('tbl_msi_leave_req','details','Detail Request')

    @api.multi
    @api.depends('employee','nik','periode_tahun')
    def _compute_nama(self):
         self.name = str(self.periode_tahun.name) + ' ' + str(self.employee.name) + ' ' + str(self.nik)

    @api.one
    @api.depends('cuti_bersama','alokasi_cuti','alokasi_cuti_sebelum','cuti_terpakai')
    def _compute_cuti_tersedia(self):
        self.cuti_tersedia = (self.alokasi_cuti + self.alokasi_cuti_sebelum) - (self.cuti_bersama + self.cuti_terpakai)

    @api.one
    @api.depends('detail')
    def _compute_cuti_terpakai(self):
        if self.detail:
           for pakai in self.detail:
               if pakai.potong_cuti:
                  self.cuti_terpakai += pakai.durasi



class tbl_msi_leave_req(models.Model):
    _name = 'tbl_msi_leave_req'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'periode_tahun desc, employee'


    details = fields.Many2one('tbl_msi_leave_allocation','Leave Allocation')
    name = fields.Char('Nomor', default='New', readonly=True)
    date = fields.Date('Date', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    periode_tahun = fields.Many2one('tbl_msi_periode_tahun','Period', required=True)
    employee = fields.Many2one('hr.employee','Employee')
    nik = fields.Char('NIK', related='employee.nik', store=True)
    dept = fields.Many2one('hr.department', 'Department', related='employee.department_id', store=True)
    divisi = fields.Many2one('tbl_employee_divisi', 'Divisi', related='employee.divisi', store=True)
    loc = fields.Many2one('tbl_employee_lokasi', 'Lokasi', related='employee.lokasi', store=True)
    job = fields.Char('Job Title', related='employee.job_title', store=True)
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')

    durasi = fields.Float('Duration')
    tipe_cuti = fields.Many2one('tbl_msi_cuti_tipe','Leave Type')
    potong_cuti = fields.Boolean('Potong Cuti', related='tipe_cuti.is_pc', store=True)
    desc = fields.Char('Desc')
    kontak_selama_cuti = fields.Char('Contact During Leave')

    state = fields.Selection([
         ('draft','Draft'),
         ('submit','Submit'),
         ('done','Approved'),
         ('cancel','Canceled')
    ], string='State', default='draft', track_visibility='onchange')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('cuti') or _('New')#

        result = super(tbl_msi_leave_req, self).create(vals)
        return result

    @api.onchange('periode_tahun')
    def _compute_periode_tahun(self):
        if self.periode_tahun:
           self.env.cr.execute('select id from tbl_msi_leave_allocation where periode_tahun = %s and employee = %s order by id desc limit 1', (self.periode_tahun.id,self.employee.id))
           for hasil in self.env.cr.fetchall():
            #raise UserError(_(hasil[0]))
               self.details = hasil[0]



    @api.onchange('start_date','end_date')
    def _compute_durasi(self):
        if self.start_date and not self.end_date:
           self.durasi = 1

        if not self.start_date and self.end_date:
           self.durasi = 0

        if self.start_date and self.end_date:
           if self.start_date == self.end_date:
              self.durasi = 0  
           if self.start_date > self.end_date:
              self.durasi = 0  
           if self.start_date < self.end_date:
              self.durasi =  self.end_date.day - self.start_date.day          

    @api.multi
    def action_submit(self):
        self.state = 'submit'


    @api.multi
    def action_approve(self):
        self.env.cr.execute('select id from tbl_msi_leave_allocation where periode_tahun = %s and employee = %s order by id desc limit 1', (self.periode_tahun.id,self.employee.id))
        for hasil in self.env.cr.fetchall():
            self.details = hasil[0]

        loop_on=0
        akhir=self.durasi
        tgl_awal=self.start_date
        while loop_on < akhir:
            tgl = tgl_awal + timedelta(days=loop_on)
            self.env.cr.execute("UPDATE tbl_msi_rekap_attendance set ket_hadir = %s, act_hadir = %s where employee = %s and sc_date_a = %s",('cuti', 'tdk_hadir', self.employee.id, tgl))
            loop_on += 1
        self.state = 'done'




