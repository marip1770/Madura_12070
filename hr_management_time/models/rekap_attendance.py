# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import *
import datetime

from odoo import api, fields, models
#from datetime import datetime, timedelta
from datetime import datetime, date, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare


class tbl_msi_rekap_attendance(models.Model):
    _name = 'tbl_msi_rekap_attendance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Rekap Attendance"
    _order = 'sc_date_in'
    _rec_name = 'employee'
 
    id_gen = fields.Char('Id Gen') 
    id_roster = fields.Char('Id Roster') 
    id_day = fields.Char('Id Shift Day')   
    employee = fields.Many2one('hr.employee','Karyawan', readonly=True)
    name = fields.Char('NIK')
    periode = fields.Many2one('tbl_msi_periode_bulan','Period', readonly=True)
    dept = fields.Many2one('hr.department', 'Department', related='employee.department_id')
    divisi = fields.Many2one('tbl_employee_divisi', 'Divisi', related='employee.divisi')
    loc = fields.Many2one('tbl_employee_lokasi', 'Lokasi', related='employee.lokasi')
    manual_jamkerja = fields.Boolean('Manual Jm Kerja', default=False, readonly=True)
    sc_name = fields.Many2one('tbl_msi_jam_kerja','Jam Kerja', help='Jam Kerja Name')
    sc_date_a = fields.Date('Tanggal', help='Jadual Tgl Masuk', readonly=True)
    sc_date_in = fields.Datetime('Jad Tgl Msk', help='Jadual Jam Masuk', readonly=True)
    sc_date_out = fields.Datetime('Jad Tgl Plg', help='Jadual Jam Pulang', readonly=True)
    is_spkl = fields.Boolean('SPKL', help='SPKL', readonly=True)
    act_date_in = fields.Datetime('Akt Tgl Msk', help='Aktual Jam Masuk', readonly=True)
    act_date_out = fields.Datetime('Akt Tgl Plg', help='Aktual Jam Pulang', readonly=True)
    toleransi = fields.Float('Toleransi (mnt)', help='Toleransi Terlambat dalam menit', readonly=True)
    late = fields.Float('Late (mnt)', help='Durasi Terlambat dalam menit', compute='_compute_late', store=True)
    max_late = fields.Float('Late Min (Jam)', help='Durasi Terlambat Mulai Kurangi Lembur')
    max_early = fields.Float('Pulcep Min (Jam)', help='Durasi Pulang Cepat Mulai Kurangi Lembur')
    early = fields.Float('Pulcep (mnt)', help='Durasi Pulang Cepat dalam menit')
    sc_hadir = fields.Selection([
        ('hadir', 'Hadir'),
        ('tdk_hadir', 'Tdk Hadir'),
        ], string='Jad Hadir', help='Jadual Kehadiran (Hadir/Tdk Hadir)', copy=False, index=True, track_visibility='onchange', readonly=True)
    act_hadir = fields.Selection([
        ('hadir', 'Hadir'),
        ('tdk_hadir', 'Tdk Hadir'),
        ], string='Akt Hadir', help='Aktual Kehadiran (Hadir/Tdk Hadir)', copy=False, index=True, track_visibility='onchange', readonly=True)

    manual_absen = fields.Boolean('Manual Absen', default=False, readonly=True)
 
    ket_hadir = fields.Selection([
        ('-', ' '),
        ('hadir', 'Hadir'),
        ('sakit', 'Sakit'),
        ('cuti', 'Cuti'),
        ('tugas_luar', 'Tugas Luar'),
        ('libur', 'Libur'),
        ('alpa', 'Alpa'),
        ('ijin', 'Ijin'),
        ('stand_by', 'Stand By'),
        ('dirumahkan', 'Dirumahkan'),
        ], string='Ket Hadir', help='Keterangan Kehadiran ((Hadir/Sakit/Cuti/Tugas Luar/Libur)', copy=False, index=True, track_visibility='onchange', readonly=True)

    nama_hari = fields.Char('Nama hari', help='Nama Hari', readonly=True)
    status_hari = fields.Selection([
        ('kerja', 'Kerja'),
        ('libur', 'Libur'),
        ('cuti_bersama', 'Cuti Bersama'),
        ], string='Status Hari', help='Status Hari (Kerja/Libur/Cuti Bersama)', compute='_compute_status_hari')
    istirahat = fields.Char('Istirahat', help='Durasi Istirahat dalam jam', readonly=True)
    durasi_kerja = fields.Char('Durasi', help='Durasi Kerja Efektif', readonly=True)
    jad_lembur = fields.Float('Jad Lembur Auto (Jam)', help='Jadual Lembur dalam jam')
    jad_lembur1 = fields.Float('Jad Lembur Auto (Jam)', help='Jadual Lembur dalam jam', compute='_compute_lembur1')
    lembur1 = fields.Float('Lembur Auto (Jam)', help='Durasi Lembur dalam jam', compute='_compute_lembur')
    lembur_spkl_start = fields.Datetime('Jad SPKL Msk', readonly=True)
    lembur_spkl_end = fields.Datetime('Jad SPKL Plg', readonly=True)
    lembur_spkl = fields.Float('Jad SPKL (Jam)', help='Durasi Lembur SPKL dalam jam', readonly=True)
    akt_lembur_spkl = fields.Float('Akt SPKL (Jam)', help='Durasi Lembur SPKL dalam jam', compute='_comp_akt_lembur_spkl', store=True,)
    total_lembur = fields.Float('Total Lembur (Jam)', help='Total Lembur dalam jam', compute='_comp_total_lembur', store=True,)
    lembur_1 = fields.Float('Lembur1', help='Total Lembur dalam jam', compute='_compute_lembur_1')
    lembur_2 = fields.Float('Lembur2', help='Total Lembur dalam jam', compute='_compute_lembur_1')
    lembur_3 = fields.Float('Lembur3', help='Total Lembur dalam jam', compute='_compute_lembur_1')
    lembur_jam = fields.Float('Lembur (Jam)', help='Durasi Lembur dalam Jam', compute='_compute_lembur_1', store=True,)
    lembur_value = fields.Float('Lembur (Value)', help='Durasi Lembur dalam Rp', compute='_compute_lembur_value', store=True,)
    ket = fields.Char('Keterangan', help='Keterangan')
    generate_id = fields.Many2one('tbl_msi_shift_gen_schedule', 'Generate Id')
    parameter_ch = fields.Char('Parameter', help='Keterangan', readonly=False)
 
      

    @api.depends('parameter_ch')
    def _compute_late(self):
        dur=0
        dur_r=0
        for record in self:
          if record.act_date_in and  record.sc_date_in: 
             if record.act_date_in >  record.sc_date_in:
                dur = record.act_date_in - record.sc_date_in
                dur_r = dur.total_seconds()/60 - record.toleransi
                record.late = dur_r


    # @api.onchange('parameter_ch')
    # def _compute_onchangelembur(self):
    #     for record in self:
    #       if record.status_hari == 'libur':
    #         record.jad_lembur = 10.5 

    @api.depends('jad_lembur','parameter_ch')
    def _compute_lembur1(self):
        for record in self:
          if record.status_hari == 'libur':
            record.jad_lembur1 = 10.5 
          if record.status_hari == 'kerja':
            record.jad_lembur1 = record.jad_lembur 

    @api.depends('parameter_ch')
    def _compute_lembur(self):
        dur=0
        dur_r=0
        for record in self:
          if record.act_date_out and  record.sc_date_out:  
            dur = record.act_date_out - record.sc_date_out
            dur_r = dur.total_seconds()/3600 - (record.late/60)

            #raise UserError(_('emp= %s jam aakhir = %s jam awal = %s dur = %s dur_r =%s') % (record.employee.name, record.act_date_out, record.sc_date_out, dur, dur_r))
            if dur_r >= 0:
               record.lembur1 = record.jad_lembur1

            else:
              if dur_r >= (record.jad_lembur1 * -1):
                 record.lembur1 =  record.jad_lembur1 + dur_r

              else:
                if dur_r < (record.jad_lembur1 * -1):
                   record.lembur1 = 0

    @api.one
    @api.depends('parameter_ch')
    def _comp_akt_lembur_spkl(self):
        if self.sc_name.name == 'Off':
          # raise UserError(_('jam_kerja= %s ') % (self.sc_name.name, ))
               self.akt_lembur_spkl = self.lembur_spkl
        
        else:   
          if self.lembur_spkl_start and self.act_date_out:
               dur = self.act_date_out - self.lembur_spkl_start
               dur_r = dur.total_seconds()/3600
               if dur_r >= self.lembur_spkl:
                  self.akt_lembur_spkl = self.lembur_spkl

               if dur_r < self.lembur_spkl: 
                  self.akt_lembur_spkl = dur_r               

          else:
                  self.akt_lembur_spkl = 0 
 

    @api.one
    @api.depends('parameter_ch')
    def _comp_total_lembur(self):
        if self.ket_hadir in ('sakit','cuti','ijin'):
          self.total_lembur = 0
        else:
          self.total_lembur = self.akt_lembur_spkl + self.lembur1


    @api.depends('parameter_ch')
    def _compute_lembur_1(self):
        for record in self:
           nn = record.total_lembur
           if nn > 0:
            if record.sc_name.name == 'Off' or record.sc_name.name == 'off' or record.sc_name.name == 'OFF': 
                 if nn > 7:
                    nn = nn - 7
                    if nn > 1:
                          nn = nn - 1
                          record.lembur_1 = 2 * 7
                          record.lembur_2 = 3 * 1
                          record.lembur_3 = 4 * nn
                          record.lembur_jam = record.lembur_1 + record.lembur_2 + record.lembur_3
                          if record.dept.kode == '27': 
                             #raise UserError(_('hasil 27'))                          
                             record.lembur_jam = 27
                          if record.dept.kode == '29': 
                             #raise UserError(_('hasil 29'))                          
                             record.lembur_jam = 29

                    else:

                       record.lembur_1 = 2 * 7
                       record.lembur_2 = 3 * nn
                       record.lembur_3 = 0
                       record.lembur_jam = record.lembur_1 + record.lembur_2 + record.lembur_3
                 else:
                       record.lembur_1 = 2 * nn
                       record.lembur_2 = 0
                       record.lembur_3 = 0
                       record.lembur_jam = record.lembur_1 + record.lembur_2 + record.lembur_3

            else: 
              if record.sc_name.kode == "N3" or record.sc_name.kode == "D6":
                 if nn > 7:
                    nn = nn - 7
                    if nn > 1:
                       nn = nn - 1
                       record.lembur_1 = 2 * 7
                       record.lembur_2 = 3 * 1
                       record.lembur_3 = 4 * nn
                       record.lembur_jam = record.lembur_1 + record.lembur_2 + record.lembur_3
                       if record.dept.kode == '27': 
                             #raise UserError(_('hasil 27'))                          
                             record.lembur_jam = 27
                       if record.dept.kode == '29': 
                             #raise UserError(_('hasil 29'))                          
                             record.lembur_jam = 29

                    else:
                       record.lembur_1 = 2 * 7
                       record.lembur_2 = 3 * nn
                       record.lembur_3 = 0
                       record.lembur_jam = record.lembur_1 + record.lembur_2 + record.lembur_3
                 else:
                       record.lembur_1 = 2 * nn
                       record.lembur_2 = 0
                       record.lembur_3 = 0
                       record.lembur_jam = record.lembur_1 + record.lembur_2 + record.lembur_3

              else:
                 if record.status_hari == 'kerja':
                    if nn > 1:
                       nn = nn - 1
                       record.lembur_1 = 1.5 * 1
                       record.lembur_2 = 2 * nn
                       record.lembur_3 = 0
                       record.lembur_jam = record.lembur_1 + record.lembur_2 + record.lembur_3
                    else:
                       record.lembur_1 = 1.5 * nn
                       record.lembur_2 = 0
                       record.lembur_3 = 0
                       record.lembur_jam = record.lembur_1 + record.lembur_2 + record.lembur_3
                 else:
                   if record.dept.kode == 'ELEKTRIFIKASI':
                       if nn > 7:
                          nn = nn - 7
                          if nn > 1:
                             record.lembur_1 = 2 * 7
                             record.lembur_2 = 3 * 1
                             record.lembur_3 = 4 * nn - 1
                             record.lembur_jam = record.lembur_1 + record.lembur_2 + record.lembur_3
                          else:

                             record.lembur_1 = 2 * 7
                             record.lembur_2 = 3 * nn
                             record.lembur_3 = 0
                             record.lembur_jam = record.lembur_1 + record.lembur_2 + record.lembur_3
                       else:
                             record.lembur_1 = 2 * nn
                             record.lembur_2 = 0
                             record.lembur_3 = 0
                             record.lembur_jam = record.lembur_1 + record.lembur_2 + record.lembur_3
                   else:
                       if nn > 7:
                          nn = nn - 7
                          if nn > 1:
                             record.lembur_1 = 2 * 7
                             record.lembur_2 = 3 * 1
                             record.lembur_3 = 4 * nn - 1
                             record.lembur_jam = record.lembur_1 + record.lembur_2 + record.lembur_3
                          else:

                             record.lembur_1 = 2 * 7
                             record.lembur_2 = 3 * nn
                             record.lembur_3 = 0
                             record.lembur_jam = record.lembur_1 + record.lembur_2 + record.lembur_3
                       else:
                             record.lembur_1 = 2 * nn
                             record.lembur_2 = 0
                             record.lembur_3 = 0
                             record.lembur_jam = record.lembur_1 + record.lembur_2 + record.lembur_3
            if record.status_hari == 'libur': 
                 if record.lembur_3 > 10:
                    if record.dept.kode == '27': 
                             #raise UserError(_('hasil 27'))                          
                             record.lembur_3 = 10
                             record.lembur_jam = 27
                    if record.dept.kode == '29': 
                             #raise UserError(_('hasil 29'))                          
                             record.lembur_3 = 12
                             record.lembur_jam = 29



           else:
                    record.lembur_1 = 0
                    record.lembur_2 = 0
                    record.lembur_3 = 0
                    record.lembur_jam = record.lembur_1 + record.lembur_2 + record.lembur_3
           # record.lembur_jam = record.lembur_1 + record.lembur_2 + record.lembur_3


    @api.depends('parameter_ch')
    def _compute_lembur_value(self):
        for record in self:
           cari = self.env['hr.contract'].search([('employee_id', '=', record.employee.id),],  order='id desc', limit=1)
           if cari:
              record.lembur_value =int( (record.lembur_jam) * (cari.wage/173))




    @api.depends('parameter_ch')
    def _compute_status_hari(self):
        dur=0
        dur_r=0
        for record in self:
           cari = self.env['tbl_msi_hari_libur'].search([('date', '=', record.sc_date_a),], limit=1)
           if cari:
              if cari.status == 'LIBUR':
                 record.status_hari = 'libur'
              else:
                 if cari.status == 'CUTI_BERSAMA':
                    record.status_hari = 'cuti_bersama'
           else:
                    record.status_hari = 'kerja'

 





class tbl_msi_proses_rekap(models.Model):
    _name = 'tbl_msi_proses_rekap'
    _description = "Proses Rekap Attendance"
    _order = 'id desc'


    name = fields.Many2one('tbl_msi_periode_bulan','Periode')
    pengecekan = fields.Char('Pengecekan')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('rekap', 'Rekap'),
        ('review', 'Review'),
        ('done', 'Done'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')




    @api.onchange('name')
    def _compute_name1(self):
        if self.name:
           cek_status = self.env['tbl_msi_proses_rekap'].sudo().search([('name', '=', self.name.id),('state', '=', 'draft')])
           if cek_status:
                  raise UserError(_('Periode %s Sudah ada dan status draft') % (self.name.name,))
        self.pengecekan = 'OK1'




    @api.one
    def action_proses(self):
        self.state='rekap'
        hasil=''
        nik=''
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        TIME_FORMAT = "%H:%M:%S"

        def get_time_from_float(float_time):
            str_time = str(float_time)
            str_hour = str_time.split('.')[0]
            str_minute = ("%2d" % int(str(float("0." + str_time.split('.')[1]) * 100).split('.')[0])).replace(' ','0')
            str_ret_time = str_hour + ":" + str_minute + ":00"
            str_ret_time = datetime.strptime(str_ret_time, TIME_FORMAT).time()
            return str_ret_time

        self.env.cr.execute("select sc_date_a, name, id, manual_absen, sc_date_out - time '4:00', sc_date_in + time '4:00',  sc_date_in - time '4:00', sc_date_out + time '4:00', sc_date_out, lembur_spkl_end + time '2:00', lembur_spkl_end  from tbl_msi_rekap_attendance where sc_date_a >= %s and sc_date_a <= %s", (self.name.date_awal,self.name.date_akhir))
        for item2 in self.env.cr.fetchall():
            hasil = item2[5]
            nik = str(item2[1]).strip()
            tanggal = hasil.strftime("%Y-%m-%d")

            hasil_out = item2[8]
            tgl_out = hasil_out.strftime("%Y-%m-%d")
            #raise UserError(_('in %s out %s jad out %s jad in %s') % (tanggal, tgl_out, hasil_out, hasil))
            #raise UserError(_("Kontrak utk pegawai %s tidak ada.") % (item2[0], item2[7], item2[4]))
            act_in='2000-01-01'
            act_out='2000-01-01'
            jam_awal=''
            jam_akhir=''
            self.env.cr.execute("select tgl_jam from tbl_msi_attendance where name = %s and tgl_jam >= %s and tgl_jam <= %s order by tgl_jam asc limit 1", (nik, item2[6], item2[5]))
            for absensi in self.env.cr.fetchall():
                act_in = absensi[0]
                #raise UserError(_('in %s out %s jad out %s jad in %s') % (tanggal, tgl_out, hasil_out, hasil))


            self.env.cr.execute("select tgl_jam from tbl_msi_attendance where name = %s  and tgl_jam >= %s and tgl_jam <= %s order by tgl_jam desc limit 1", (nik, item2[4], item2[7]))
            for absensi_out in self.env.cr.fetchall():
                act_out = absensi_out[0]

            if act_in == '2000-01-01' and act_out == '2000-01-01':
               hadir = 'tdk_hadir'
               ket_hadir = 'alpa'
            else:
               hadir = 'hadir'
               ket_hadir = '-'

            if act_in == act_out:
               hadir = 'tdk_hadir'

             
            if not item2[3]:
               self.env.cr.execute("update tbl_msi_rekap_attendance set act_date_in = %s, act_date_out = %s, act_hadir = %s, ket_hadir = %s where id = %s", (act_in, act_out, hadir, ket_hadir, item2[2]))


    @api.one
    def action_rekap(self):
        self.state='review'
        cari_param = self.env['tbl_msi_rekap_attendance'].sudo().search([('sc_date_a', '>=', self.name.date_awal),('sc_date_a', '<=', self.name.date_akhir)] )
        if cari_param:
           for seting in cari_param:
               seting.parameter_ch = fields.Datetime.now()

    @api.one
    def action_ulang(self):
        self.state='draft'


         
    @api.one
    def action_close(self):
        self.state='done'            


