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


class tbl_payrol_raw(models.Model):
    _name = 'tbl_payrol_raw'
    _description = "tbl_payrol_raw"
    _order = 'dept, name, date'

   
    employee = fields.Many2one('hr.employee','Employee', readonly=True)
    name = fields.Char('NIK', related='employee.nik', store=True)
    dept = fields.Many2one('hr.department', 'Department', related='employee.department_id', store=True)
    divisi = fields.Many2one('tbl_employee_divisi', 'Divisi', related='employee.divisi', store=True)
    loc = fields.Many2one('tbl_employee_lokasi', 'Lokasi', related='employee.lokasi', store=True)
    job = fields.Char('Job Title', related='employee.job_title', store=True)

    date = fields.Date('Date', help='Tanggal Jadual', readonly=True)

    late = fields.Float('Late (mnt)', help='Durasi Terlambat dalam menit', readonly=True)
    early = fields.Float('Pulang Cepat (mnt)', help='Durasi Pulang Cepat dalam menit', readonly=True)
    details = fields.Many2one('tbl_payrol_proses_raw','Detail')
    nama_hari = fields.Char('Nama hari', help='Nama Hari', readonly=True)
    status_hari = fields.Char('Status Hari', help='Status Hari', readonly=True)
    nominal = fields.Float('Nominal', help='Nominal Lembur', compute="_compute_nominal", store=True)
    hadir = fields.Float('Hadir', default=1)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('data', 'Data'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ('cancel', 'Cancel'),
        ], string='Status', related='details.state', store=True, readonly=False)
    tipe = fields.Selection([
        ('attendance', 'Attendance'),
        ('cuti', 'Cuti'),
        ('hour', 'Hourmeter'),
        ('retase', 'Retase'),
        ('kinerja', 'Kinerja'),
        ('sanksi', 'Saksi/Penghargaam'),
        ('potongan', 'Potongan'),
        ('loan', 'Pinjaman'),
        ('lembur', 'Lembur'),
        ('lainnya', 'Lainnya'),
        ], string='Tipe', readonly=True)
    act_hadir = fields.Selection([
        ('hadir', 'Hadir'),
        ('tdk_hadir', 'Tdk Hadir'),
        ], string='Akt Hadir', help='Aktual Kehadiran (Hadir/Tdk Hadir)',readonly=True)



class tbl_payrol_proses_raw(models.Model):
    _name = 'tbl_payrol_proses_raw'
    _description = "tbl_payrol_proses_raw"
    _order = 'date desc'

    name = fields.Char('Name', compute="_compute_nama", store=True) 
    date = fields.Date('Date', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    periode = fields.Many2one('tbl_payroll_period','Period')  
    ket = fields.Char('Keterangan') 
    state = fields.Selection([
        ('draft', 'Draft'),
        ('data', 'Data'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ('cancel', 'Cancel'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    detail = fields.One2many('tbl_payrol_raw','details','Detail')


    @api.one
    @api.depends('periode')
    def _compute_nama(self):
        if self.periode:
           self.name = 'PROSES PAYROLL ' + str(self.periode.name).upper() 


    def action_submit(self):
        self.state = 'submit'


    def action_cancel(self):
        self.state = 'cancel'

   ##### Proses Attendance
   #####

    def action_get_att(self):
        raw_obj = self.env['tbl_payrol_raw']
        gaji=0
        
        if not self.periode:
           raise UserError(_("Periode belum diisi"))

        if self.detail:
           self.env.cr.execute('delete from tbl_payrol_raw where tipe = %s and details= %s', ('attendance', self.id))

        self.env.cr.execute('select employee, name, id, id, id, sc_date_a, late, early, lembur_value, act_hadir from tbl_msi_rekap_attendance \
                             where sc_date_a >= %s and sc_date_a <= %s and act_hadir = %s', (self.periode.date_awal, self.periode.date_akhir,'hadir') )
        for hasil in self.env.cr.fetchall():
                  data_line2 = raw_obj.create({
                      'details': self.id,
                      'employee': hasil[0],
                      'tipe': 'attendance',
                      'name': hasil[1],
                      # 'dept': hasil[2],
                      'date': hasil[5],
                      'late': hasil[6],
                      'early': hasil[7],
                      'nominal': hasil[8],
                      'act_hadir': hasil[9],
                  })



    def action_get_lembur(self):
        raw_obj = self.env['tbl_payrol_raw']
        gaji=0
        
        if not self.periode:
           raise UserError(_("Periode belum diisi"))

        if self.detail:
           self.env.cr.execute('delete from tbl_payrol_raw where tipe = %s and details= %s', ('lembur', self.id))

        self.env.cr.execute('select employee, name, id, id, id, sc_date_a, late, early, lembur_value, act_hadir from tbl_msi_rekap_attendance \
                             where sc_date_a >= %s and sc_date_a <= %s and act_hadir = %s', (self.periode.date_awal, self.periode.date_akhir,'hadir') )
        for hasil in self.env.cr.fetchall():
                  data_line2 = raw_obj.create({
                      'details': self.id,
                      'employee': hasil[0],
                      'tipe': 'lembur',
                      'name': hasil[1],
                      # 'dept': hasil[2],
                      'date': hasil[5],
                      'late': hasil[6],
                      'early': hasil[7],
                      'nominal': hasil[8],
                      'act_hadir': hasil[9],
                  })

        self.env.cr.execute('select employee, name, id, id, id, sc_date_a, late, early, lembur_value, act_hadir from tbl_msi_rekap_attendance \
                             where sc_date_a >= %s and sc_date_a <= %s and act_hadir = %s and lembur_spkl_end IS NOT NULL', (self.periode.date_awal, self.periode.date_akhir,'tdk_hadir') )
        for hasil1 in self.env.cr.fetchall():
                  data_line2 = raw_obj.create({
                      'details': self.id,
                      'employee': hasil1[0],
                      'tipe': 'lembur',
                      'name': hasil1[1],
                      # 'dept': hasil1[2],
                      'date': hasil1[5],
                      'late': hasil1[6],
                      'early': hasil1[7],
                      'nominal': hasil1[8],
                      'act_hadir': hasil[9],
                  })




   ##### Proses Retase Transport
   #####

    def action_get_retase(self):
        raw_obj = self.env['tbl_payrol_raw']
        
        if not self.periode:
           raise UserError(_("Periode belum diisi"))

        if self.detail:
           self.env.cr.execute('delete from tbl_payrol_raw where tipe = %s and details= %s', ('retase', self.id))

        self.env.cr.execute('select date, employee, nominal from tbl_msi_retase \
                             where date >= %s and date <= %s', (self.periode.date_awal, self.periode.date_akhir) )
        for hasil in self.env.cr.fetchall():
                  data_line2 = raw_obj.create({
                      'details': self.id,
                      'employee': hasil[1],
                      'tipe': 'retase',
                      'date': hasil[0],
                      'nominal': hasil[2],
                  })
   ##### Proses Retase Driver /Kinerja
   #####

    def action_get_kinerja(self):
        raw_obj = self.env['tbl_payrol_raw']
        
        if not self.periode:
           raise UserError(_("Periode belum diisi"))

        if self.detail:
           self.env.cr.execute('delete from tbl_payrol_raw where tipe = %s and details= %s', ('kinerja', self.id))

        self.env.cr.execute('select date, id_employee, nominal from tbl_msi_retase_driver \
                             where date >= %s and date <= %s', (self.periode.date_awal, self.periode.date_akhir) )
        for hasil in self.env.cr.fetchall():
                  data_line2 = raw_obj.create({
                      'details': self.id,
                      'employee': hasil[1],
                      'tipe': 'kinerja',
                      'date': hasil[0],
                      'nominal': hasil[2],
                  })

   ##### Proses Hourmeter
   #####

    def action_get_hm(self):
        raw_obj = self.env['tbl_payrol_raw']
        
        if not self.periode:
           raise UserError(_("Periode belum diisi"))

        if self.detail:
           self.env.cr.execute('delete from tbl_payrol_raw where tipe = %s and details= %s', ('hour', self.id))

        self.env.cr.execute('select date, employee, nominal from tbl_msi_hourmeter \
                             where date >= %s and date <= %s', (self.periode.date_awal, self.periode.date_akhir) )
        for hasil in self.env.cr.fetchall():
                  data_line2 = raw_obj.create({
                      'details': self.id,
                      'employee': hasil[1],
                      'tipe': 'hour',
                      'date': hasil[0],
                      'nominal': hasil[2],
                  })



    def action_approve(self):
      cari_data = self.env['tbl_payrol_proses_raw'].sudo().search([('periode', '=', self.periode.id),('state', '=', 'approve')] )
      if cari_data:
        raise UserError(_('Periode %s Sudah ada dan status Approve') % (self.periode.name,))
      self.state = 'approve'



class tbl_payrol_raw_import(models.Model):
    _name = 'tbl_payrol_raw_import'
    _description = "tbl_payrol_raw_import"
    _order = 'periode, name'

   
    employee = fields.Many2one('hr.employee','Employee')
    name = fields.Char('NIK')
    date = fields.Date('Tanggal', help='Tanggal Input')
    periode = fields.Many2one('tbl_payroll_period','Period')  


    gapok = fields.Float('Gaji Pokok')
    jabatan = fields.Float('Jabatan')
    tanggung_jawab = fields.Float('Tanggung Jawab')

    hm = fields.Float('HM', help='HM')
    retase = fields.Float('Retase', help='Retase')
    lembur = fields.Float('Lembur', help='Uang lembur')
    hadir = fields.Float('Hadir', help='Tunjangan Kehadiran')
    kinerja = fields.Float('Kinerja', help='Tunjangan Kinerja')
    transport = fields.Float('Transport', help='Uang Transport')
    bersih_unit = fields.Float('Kebersihan Unit')
    uang_saku = fields.Float('Uang Saku')
    makan = fields.Float('Uang Makan')
    field = fields.Float('Field', help='Tunjangan Field')
    komunikasi = fields.Float('Komunikasi', help='Tunjangan Komunikasi')
    bonus = fields.Float('Bonus', help='Bonus')
    pab = fields.Float('T PAB')
    hd = fields.Float('T HD')
    se = fields.Float('T SE')
    spkl = fields.Float('SPKL')
    a_pph21 = fields.Float('T PPH21')
    a_jk = fields.Float('T JK')
    a_jkk = fields.Float('T JKK')
    a_jkm = fields.Float('T JKM')
    a_jht = fields.Float('T JHT')
    a_jp = fields.Float('T JP')
    a_bpjs_kesehatan = fields.Float('T BPJS Kshtan')

    d_jht = fields.Float('P JHT')
    d_jp = fields.Float('P JHT')
    d_bpjs_kesehatan = fields.Float('P BPJS Kshtan')
    d_bpjs_tenagakerja = fields.Float('P BPJS Tng Kerja')
    d_pph21 = fields.Float('P PPH21')
    d_lainnya = fields.Float('P Lainnya')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('data', 'Data'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ], string='Status', readonly=False)


    @api.one
    @api.depends('gaji','lembur')
    def _compute_nominal(self):
        self.nominal = self.gaji * self.lembur

