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


class tbl_msi_time_pindah_jadual(models.Model):
    _name = 'tbl_msi_time_pindah_jadual'
    _description = "Pindah Jadual"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

   
    name = fields.Char('Nomor', default='New', readonly=True)
    date = fields.Date('Date', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    employee = fields.Many2one('hr.employee','Employee', track_visibility='onchange')
    nik =  fields.Char('NIK', related='employee.nik', store=True)
    jadual_baru = fields.Date('Tanggal', track_visibility='onchange')
    jam_kerja = fields.Many2one('tbl_msi_jam_kerja', 'Jam Kerja')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('done', 'Approved'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    @api.one
    def action_submit(self):
        self.state = 'submit'

    @api.one
    def action_ulang(self):
        self.state = 'draft'


 
    @api.one
    def action_approve(self):
        self.state = 'done'
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        TIME_FORMAT = "%H:%M:%S"



        def get_time_from_float(float_time):
            str_time = str(float_time)
            str_hour = str_time.split('.')[0]
            str_minute = ("%2d" % int(str(float("0." + str_time.split('.')[1]) * 100).split('.')[0])).replace(' ','0')
            str_ret_time = str_hour + ":" + str_minute + ":00"
            str_ret_time = datetime.strptime(str_ret_time, TIME_FORMAT).time()
            return str_ret_time


        cari2 = self.env['tbl_msi_rekap_attendance'].search(
                    [('employee', '=', self.employee.id),
                    ('sc_date_a', '=', self.jadual_baru)], limit=1)
        if cari2:
                   cari2.manual_jamkerja = True
                   cari2.sc_name = self.jam_kerja.id
                   cari2.sc_date_in = (datetime.combine(self.jadual_baru,get_time_from_float(self.jam_kerja.jam_in))) - timedelta(hours=7)
                   cari2.sc_date_out = (datetime.combine(self.jadual_baru,get_time_from_float(self.jam_kerja.jam_out))) - timedelta(hours=7)
                   cari2.toleransi = self.jam_kerja.tol_terlambat
                   cari2.parameter_ch = fields.Datetime.now()
        else:
                   raise UserError(_('Tidak ada dalam Rekap'))

 

class tbl_msi_time_manual(models.Model):
    _name = 'tbl_msi_time_manual'
    _description = "Manual Absensi"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    name = fields.Char('Nomor', default='New', readonly=True)
    date = fields.Date('Date', default=fields.Date.today(), readonly=True)
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user , readonly=True)
    type = fields.Selection([
        ('employee', 'Employee'),
        ('group', 'Group'),
        ], string='Type', copy=False, index=True, track_visibility='onchange', default='employee')
    employee = fields.Many2one('hr.employee','Employee', track_visibility='onchange')
    nik =  fields.Char('NIK', related='employee.nik', store=True)
    group1 = fields.Many2one('tbl_msi_employee_group','Group')
    tanggal_ubah = fields.Date('Date Change', track_visibility='onchange')
    tanggal_ubah_awal = fields.Datetime('jam awal')
    tanggal_ubah_akhir = fields.Datetime('jam_akhir')
    jenis_ubah = fields.Selection([
        ('kehadiran', 'Kehadiran'),
        ('absensi', 'Absensi'),
        ], string='Type',required=True, copy=False, index=True, track_visibility='onchange')
    act_date_in = fields.Datetime('Actual Date In', help='Aktual Jam Masuk')
    act_date_out = fields.Datetime('Actual Date Out', help='Aktual Jam Pulang')
    periode_tahun = fields.Many2one('tbl_msi_periode_tahun','Period', compute='_compute_periode', store=True,)
    absensi = fields.Selection([
        ('sakit', 'Sakit'),
        ('cuti', 'Cuti'),
        ('tugas_luar', 'Tugas Luar'),
        ('libur', 'Libur'),
        ('alpa', 'Alpa'),
        ('ijin', 'Ijin'),
        ], string='Ket Hadir', help='Keterangan Kehadiran ((Hadir/Sakit/Cuti/Tugas Luar/Libur)', copy=False, index=True, track_visibility='onchange')
    ket = fields.Char('Keterangan')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('verify', 'Verifify'),
        ('approve', 'Approved'),
        ('done', 'Done'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

 
    @api.multi
    @api.depends('tanggal_ubah')
    def _compute_periode(self):
        out=0
        for rec in self:
          if rec.tanggal_ubah:
             cari = self.env['tbl_msi_periode_tahun'].search([('date_awal','<=', rec.tanggal_ubah),('date_akhir','>=', rec.tanggal_ubah)])
             if cari:
                rec.periode_tahun = cari.id
             else:
                raise UserError(_('Pembuatan Periode Tahun belum dilakukan'))

    @api.one
    def action_submit(self):
        self.state = 'submit'


    @api.one
    def action_ulang(self):
        self.state = 'draft'


    @api.one
    def action_verify(self):
        self.state = 'verify'


    @api.one
    def action_approve(self):
        self.state = 'approve'


    @api.one
    def action_done(self):
        self.state = 'done'
        if self.jenis_ubah == 'kehadiran':
          if self.type == 'employee':         
             if self.act_date_in and not self.act_date_out:
                cari2 = self.env['tbl_msi_rekap_attendance'].search(
                    [('employee', '=', self.employee.id),
                    ('sc_date_a', '=', self.tanggal_ubah)], limit=1)
                if cari2:
                   cari2.act_date_in = self.act_date_in
                   cari2.manual_absen = True
                   cari2.act_hadir = 'hadir'
                   cari2.ket_hadir = '-'
                   cari2.parameter_ch = fields.Datetime.now()
                else:
                   raise UserError(_('Tidak ada dalam Rekap'))

             if not self.act_date_in and self.act_date_out:
                cari2 = self.env['tbl_msi_rekap_attendance'].search(
                    [('employee', '=', self.employee.id),
                    ('sc_date_a', '=', self.tanggal_ubah)], limit=1)
                if cari2:
                   cari2.act_date_out = self.act_date_out
                   cari2.manual_absen = True
                   cari2.act_hadir = 'hadir'
                   cari2.ket_hadir = '-'
                   cari2.parameter_ch = fields.Datetime.now()
                else:
                   raise UserError(_('Tidak ada dalam Rekap'))


             if self.act_date_in and self.act_date_out:
                cari2 = self.env['tbl_msi_rekap_attendance'].search(
                    [('employee', '=', self.employee.id),
                    ('sc_date_a', '=', self.tanggal_ubah)], limit=1)
                if cari2:
                   cari2.act_date_out = self.act_date_out
                   cari2.act_date_in = self.act_date_in
                   cari2.manual_absen = True
                   cari2.act_hadir = 'hadir'
                   cari2.ket_hadir = '-'
                   cari2.parameter_ch = fields.Datetime.now()
                else:
                   raise UserError(_('Tidak ada dalam Rekap'))

          if self.type == 'group':         
             if self.act_date_in and not self.act_date_out:
                for emp in self.group1.detail:
                   cari2 = self.env['tbl_msi_rekap_attendance'].search(
                       [('employee', '=', emp.employee.id),
                       ('sc_date_a', '=', self.tanggal_ubah)], limit=1)
                   if cari2:
                      cari2.act_date_in = self.act_date_in
                      cari2.manual_absen = True
                      cari2.act_hadir = 'hadir'
                      cari2.ket_hadir = '-'
                      cari2.parameter_ch = fields.Datetime.now()
                   else:
                      raise UserError(_('Tidak ada dalam Rekap'))

             if not self.act_date_in and self.act_date_out:
                for emp in self.group1.detail:
                   cari2 = self.env['tbl_msi_rekap_attendance'].search(
                       [('employee', '=', emp.employee.id),
                       ('sc_date_a', '=', self.tanggal_ubah)], limit=1)
                   if cari2:
                      cari2.act_date_out = self.act_date_out
                      cari2.manual_absen = True
                      cari2.act_hadir = 'hadir'
                      cari2.ket_hadir = '-'
                      cari2.parameter_ch = fields.Datetime.now()
                   else:
                      raise UserError(_('Tidak ada dalam Rekap'))
 

             if self.act_date_in and self.act_date_out:
                for emp in self.group1.detail:
                   cari2 = self.env['tbl_msi_rekap_attendance'].search(
                       [('employee', '=', emp.employee.id),
                       ('sc_date_a', '=', self.tanggal_ubah)], limit=1)
                   if cari2:
                      cari2.act_date_out = self.act_date_out
                      cari2.act_date_in = self.act_date_in
                      cari2.manual_absen = True
                      cari2.act_hadir = 'hadir'
                      cari2.ket_hadir = '-'
                      cari2.parameter_ch = fields.Datetime.now()
                   else: 
                      raise UserError(_('Employee "%s" Tidak ada daam rekap' % (emp.employee.name, )))
 
        if self.jenis_ubah == 'absensi':
                self.env.cr.execute("update tbl_msi_rekap_attendance set ket_hadir = %s, act_hadir = %s, manual_absen = %s where employee = %s and sc_date_a = %s",(self.absensi, 'tdk_hadir', True, self.employee.id, self.tanggal_ubah))
                cari_param = self.env['tbl_msi_rekap_attendance'].sudo().search([('employee', '=', self.employee.id),('sc_date_a', '=', self.tanggal_ubah)], limit=1 )
                if cari_param:
                   cari_param.parameter_ch = fields.Datetime.now()

                if self.absensi in ('ijin','cuti'):
                   cuti=0
                   cuti_r=0
                   cari = self.env['tbl_msi_leave_allocation'].search([('periode_tahun','=', self.periode_tahun.id),('employee','=', self.employee.id)], limit=1)
                   if cari:
                      cuti = cari.id

                   cari_cuti = self.env['tbl_msi_cuti_tipe'].search([('name','=', 'CUTI TAHUNAN 12')], limit=1)
                   if cari_cuti:
                      cuti_r = cari_cuti.id
                   else: 
                      raise UserError(_('Tidak ada cuti tahunan dengan nama CUTI TAHUNAN 12'))


                   leave_obj = self.env['tbl_msi_leave_req']
                   leave = leave_obj.create({
                          'details': cuti,
                          'name': self.env['ir.sequence'].next_by_code('cuti'),
                          'date': self.date,
                          'user': self.user.id,
                          'periode_tahun': self.periode_tahun.id,
                          'employee': self.employee.id,
                          'start_date': self.tanggal_ubah,
                          'end_date': self.tanggal_ubah,
                          'tipe_cuti': cuti_r,
                          'durasi': 1,
                          'desc': 'Pengajuan Ijin Tidak Masuk',
                   })

                if self.absensi == 'sakit':
                   cari2 = self.env['tbl_msi_rekap_attendance'].search(
                       [('employee', '=', self.employee.id),
                       ('sc_date_a', '=', self.tanggal_ubah)], limit=1)
                   if cari2:
                      cari2.manual_absen = True
                      cari2.act_hadir = 'tdk_hadir'
                      cari2.ket_hadir = 'sakit'
                      cari2.parameter_ch = fields.Datetime.now()
                   else: 
                      raise UserError(_('Employee "%s" Tidak ada daam rekap' % (self.employee.name, )))

                if self.absensi == 'tugas_luar':
                   cari2 = self.env['tbl_msi_rekap_attendance'].search(
                       [('employee', '=', emp.employee.id),
                       ('sc_date_a', '=', self.tanggal_ubah)], limit=1)
                   if cari2:
                      cari2.manual_absen = True
                      cari2.act_hadir = 'hadir'
                      cari2.ket_hadir = 'tugas_luar'
                      cari2.parameter_ch = fields.Datetime.now()
                   else: 
                      raise UserError(_('Employee "%s" Tidak ada daam rekap' % (emp.employee.name, )))

                if self.absensi == 'libur':
                   cari2 = self.env['tbl_msi_rekap_attendance'].search(
                       [('employee', '=', emp.employee.id),
                       ('sc_date_a', '=', self.tanggal_ubah)], limit=1)
                   if cari2:
                      cari2.manual_absen = True
                      cari2.act_hadir = 'tdk_hadir'
                      cari2.ket_hadir = 'libur'
                      cari2.parameter_ch = fields.Datetime.now()
                   else: 
                      raise UserError(_('Employee "%s" Tidak ada daam rekap' % (emp.employee.name, )))

                if self.absensi == 'alpa':
                   cari2 = self.env['tbl_msi_rekap_attendance'].search(
                       [('employee', '=', emp.employee.id),
                       ('sc_date_a', '=', self.tanggal_ubah)], limit=1)
                   if cari2:
                      cari2.manual_absen = True
                      cari2.act_hadir = 'tdk_hadir'
                      cari2.ket_hadir = 'alpa'
                      cari2.parameter_ch = fields.Datetime.now()
                   else: 
                      raise UserError(_('Employee "%s" Tidak ada daam rekap' % (emp.employee.name, )))




