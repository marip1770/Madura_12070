# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import *
import datetime
import math

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


class tbl_msi_shift_gen_schedule(models.Model):
    _name = 'tbl_msi_shift_gen_schedule'
    _description = "Gen Schedule"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

   
    name = fields.Char('Nomor', default='New', readonly=True)
    date = fields.Date('Date', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    periode = fields.Many2one('tbl_msi_periode_bulan','Period', required=True)
    date_awal = fields.Date('Date Start')
    date_akhir = fields.Date('Date End')
    ket = fields.Char('Ket')
    ref = fields.Char('Ref')
    type = fields.Selection([
        ('employee', 'Employee'),
        ('group', 'Group'),
        ], string='Type', copy=False, index=True, track_visibility='onchange', default='employee')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ('generate', 'Generated'),
        ('done', 'Done'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    employee = fields.Many2one('hr.employee','Employee', track_visibility='onchange')
    nik =  fields.Char('NIK', related='employee.nik', store=True)
    roster = fields.Many2one('tbl_msi_shift','Roster', required=True)
    group1 = fields.Many2one('tbl_msi_employee_group','Group')
    group = fields.One2many('tbl_gen_jadual_group','details','Group')
    jam_kerja = fields.One2many('tbl_gen_jadual_jam_kerja','details','Jam Kerja')
    jml_group = fields.Float('Jml group', compute='_compute_group', store=True)
    jml_jam_kerja = fields.Float('Jml jam kerja', compute='_compute_jam_kerja', store=True)


    @api.onchange('group1')
    def _onchange_group11(self):
        if self.group1:
           if not self.periode:
              raise UserError(_('Periode harus diisi'))
           cek_status = self.env['tbl_msi_shift_gen_schedule'].sudo().search([('periode', '=', self.periode.id),('group1', '=', self.group1.id),('state', 'in', ('generate','done'))])
           if cek_status:
                  raise UserError(_('Periode %s dan grup %s Sudah ada') % (self.periode.name, self.group1.name))


    @api.onchange('employee')
    def _onchange_employee1(self):
        if self.employee:
           if not self.periode:
              raise UserError(_('Periode harus diisi'))
           cek_status = self.env['tbl_msi_shift_gen_schedule'].sudo().search([('periode', '=', self.periode.id),('employee', '=', self.employee.id),('state', 'in', ('generate','done'))])
           if cek_status:
                  raise UserError(_('Periode %s dan Employee %s Sudah ada') % (self.periode.name, self.employee.name))


    @api.onchange('periode')
    def _onchange_periode1(self):
        if self.periode:
           if self.employee:
              cek_status = self.env['tbl_msi_shift_gen_schedule'].sudo().search([('periode', '=', self.periode.id),('employee', '=', self.employee.id),('state', 'in', ('generate','done'))])
              if cek_status:
                  raise UserError(_('Periode %s dan Employee %s Sudah ada') % (self.periode.name, self.employee.name))
           if self.group1:
              cek_status = self.env['tbl_msi_shift_gen_schedule'].sudo().search([('periode', '=', self.periode.id),('group1', '=', self.group1.id),('state', 'in', ('generate','done'))])
              if cek_status:
                  raise UserError(_('Periode %s dan grup %s Sudah ada') % (self.periode.name, self.group1.name))



 
    @api.one
    @api.depends('group')
    def _compute_group(self):
        for hitung in self.group:
            self.jml_group += hitung.jml

    @api.one
    @api.depends('jam_kerja')
    def _compute_jam_kerja(self):
        for hitung in self.jam_kerja:
            self.jml_jam_kerja += hitung.jml


    def action_submit(self):
        if self.type == 'group':
           if not self.group1:
               raise UserError(_('Group harus diisi'))
        if self.type == 'employee':
           if not self.employee:
              raise UserError(_('Employee harus diisi'))

        if self.periode:
           if self.employee:
              cek_status = self.env['tbl_msi_shift_gen_schedule'].sudo().search([('periode', '=', self.periode.id),('employee', '=', self.employee.id),('create_date', '<', self.create_date),('state', 'in', ('generate','done'))])
              if cek_status:
                  raise UserError(_('Periode %s dan Employee %s Sudah ada') % (self.periode.name, self.employee.name))
           if self.group1:
              cek_status = self.env['tbl_msi_shift_gen_schedule'].sudo().search([('periode', '=', self.periode.id),('group1', '=', self.group1.id),('create_date', '<', self.create_date),('state', 'in', ('generate','done'))])
              if cek_status:
                  raise UserError(_('Periode %s dan grup %s Sudah ada') % (self.periode.name, self.group1.name))

        self.state = 'submit'

    def action_approve(self):
        self.state = 'approve'

    def action_done(self):
        self.state = 'done'

    @api.one
    def action_generate(self):
        schedule_obj = self.env['tbl_msi_shift_schedule']
        epoch_year = date.today().year
        year_end = date(epoch_year, 12, 31)
        year_e = year_end - self.periode.date_awal
        loop_periode = round(year_e.days) + 1
        #raise UserError(_('year end :%s awal :%s loop :%s') % (year_end, self.periode.date_awal, loop_periode))

        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        TIME_FORMAT = "%H:%M:%S"
        self.state = 'generate'


        def get_time_from_float(float_time):
            str_time = str(float_time)
            str_hour = str_time.split('.')[0]
            str_minute = ("%2d" % int(str(float("0." + str_time.split('.')[1]) * 100).split('.')[0])).replace(' ','0')
            str_ret_time = str_hour + ":" + str_minute + ":00"
            str_ret_time = datetime.strptime(str_ret_time, TIME_FORMAT).time()
            return str_ret_time

        def float_time_convert(float_val):
           factor = float_val < 0 and -1 or 1
           val = abs(float_val)
           return (factor * int(math.floor(val)), int(round((val % 1) * 60)))


        if self.type == 'group':
           if not self.group1:
              raise UserError(_('Group harus diisi'))

           if not self.group1.detail:
              raise UserError(_('Nama Pegawai pada Group harus diisi'))

           if not self.roster:
              raise UserError(_('Roster harus diisi'))

           if not self.roster.detail and not self.roster.detail_hari:
              raise UserError(_('Detail Jam Kerja pada Roster harus diisi'))

           else:
              self.env.cr.execute("delete from tbl_msi_shift_schedule where id_gen = %s", (str(self.id),))
              self.env.cr.execute("delete from tbl_msi_rekap_attendance where id_gen = %s", (str(self.id),))

              #self.env.cr.execute("delete from tbl_msi_rekap_attendance where id_gen = %s", (str(self.id),))

              for emp in self.group1.detail:
                  if not emp.employee.id:
                     raise UserError(_('Nama Karyawan pada grup shift ada yg belum diisi'))
                  #self.env.cr.execute("select * from tbl_msi_rekap_attendance where sc_date_a = %s and employee = %s", (self.periode.date_awal, emp.employee.id))
                  #item = self.env.cr.fetchall()
                  #if item:
                  self.env.cr.execute("delete from tbl_msi_rekap_attendance where sc_date_a >= %s and employee = %s", (self.periode.date_awal, emp.employee.id))
                 # self.env.cr.execute("INSERT into tbl_msi_shift_schedule (id_gen, employee, name, dept, divisi, loc, periode) values (%s,%s,%s,%s,%s,%s,%s)",(self.id, emp.employee.id, emp.employee.nik, emp.employee.department_id.id, emp.employee.divisi.id, emp.employee.lokasi.id, self.periode.id))

                  self.env.cr.execute("INSERT into tbl_msi_shift_schedule (id_gen, employee, name, periode) values (%s,%s,%s,%s)",(self.id, emp.employee.id, emp.employee.nik, self.periode.id))

                  kerja=''
                  loop_start=0
                  loop_jam=-1
                  skrg=0
                  sc_hadir=''
                  nama_hari=''
                  #raise UserError(_('loop start :%s periode loop :%s') % (loop_start, loop_periode))

                  c=date.today().day
                  b=date.today().month
                  a=date.today().year
                  d=a+b+c

                  while loop_start <= loop_periode :
                    id_roster = self.roster.id + d
                    if self.roster.reguler == False:
                      for emp_sc in self.roster.detail:                         
                        loop_start += 1
                        loop_jam += 1
 
                        jam_awal = get_time_from_float(emp_sc.name.jam_in)
                        jam_akhir = get_time_from_float(emp_sc.name.jam_out)
                        tgl_awal = self.periode.date_awal + timedelta(days=int(loop_jam))
                        if tgl_awal <= year_end:
                          sc_in = (datetime.combine(tgl_awal,jam_awal)) - timedelta(hours=7),

                          if emp_sc.name.overnight:                          
                             sc_out = (datetime.combine((tgl_awal + timedelta(days=1)),jam_akhir)) - timedelta(hours=7),
                          else:                          
                             sc_out = (datetime.combine(tgl_awal,jam_akhir)) - timedelta(hours=7),
                          
                          if str(emp_sc.name.name) == 'OFF' or str(emp_sc.name.name) == 'Off':
                            sc_hadir = 'tdk_hadir'
                            kerja = 'libur'
                          else:
                            sc_hadir = 'hadir'
                            kerja = 'kerja'
                          skrg = tgl_awal.weekday()
                             
                          self.env.cr.execute("INSERT into tbl_msi_rekap_attendance (id_day, id_roster, id_gen, employee, name, periode, sc_name, sc_date_in, sc_date_out, toleransi, max_late, max_early, \
                                                                          sc_hadir, nama_hari, durasi_kerja, jad_lembur, sc_date_a ) \
                                                                          values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)\
                                                                         ",(emp_sc.siklus, id_roster,self.id, emp.employee.id, emp.employee.nik, self.periode.id, emp_sc.name.id, sc_in, sc_out, emp_sc.name.tol_terlambat, emp_sc.name.max_lama_terlambat, emp_sc.name.min_lama_cepat_pulang, sc_hadir, nama_hari, emp_sc.name.durasi, emp_sc.name.overtime, tgl_awal))

                    if self.roster.reguler == True:
                      # raise UserError(_('Reguler True'))
                      #for emp_hr in self.roster.detail_hari:                         
                        loop_start += 1
                        loop_jam += 1
 
                        tgl_awal = self.periode.date_awal + timedelta(days=int(loop_jam))
                        if tgl_awal <= year_end:
                          skrg = tgl_awal.weekday()
                          cek_hari = self.env['tbl_msi_shift_detail_hari'].sudo().search([('details', '=', self.roster.id),('name', '=', str(skrg))], limit = 1)
                          if cek_hari:
                             jam_awal_0 = str(timedelta(hours=cek_hari.jam_kerja.jam_in))
                             jam_awal = datetime.strptime(jam_awal_0, TIME_FORMAT).time()
                             jam_akhir_0 = str(timedelta(hours=cek_hari.jam_kerja.jam_out))
                             jam_akhir = datetime.strptime(jam_akhir_0, TIME_FORMAT).time()

                             sc_in = (datetime.combine(tgl_awal,jam_awal)) - timedelta(hours=7),
                             #raise UserError(_(jam_awal3))

                             if cek_hari.jam_kerja.overnight:                          
                                sc_out = (datetime.combine((tgl_awal + timedelta(days=1)),jam_akhir)) - timedelta(hours=7),
                             else:                          
                                sc_out = (datetime.combine(tgl_awal,jam_akhir)) - timedelta(hours=7),
                          
                             if str(cek_hari.jam_kerja.name) == 'OFF' or str(cek_hari.jam_kerja.name) == 'Off':
                                 sc_hadir = 'tdk_hadir'
                                 kerja = 'libur'
                             else:
                                 sc_hadir = 'hadir'
                                 kerja = 'kerja'
                             
                             self.env.cr.execute("INSERT into tbl_msi_rekap_attendance (id_gen, employee, name, periode, sc_name, sc_date_in, sc_date_out, toleransi, max_late, max_early, \
                                                                          sc_hadir, nama_hari, durasi_kerja, jad_lembur, sc_date_a ) \
                                                                          values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)\
                                                                         ",(self.id, emp.employee.id, emp.employee.nik, self.periode.id, cek_hari.jam_kerja.id, sc_in, sc_out, cek_hari.jam_kerja.tol_terlambat, cek_hari.jam_kerja.max_lama_terlambat, cek_hari.jam_kerja.min_lama_cepat_pulang, sc_hadir, nama_hari, cek_hari.jam_kerja.durasi, cek_hari.jam_kerja.overtime, tgl_awal))


                    id_roster = id_roster + 1
        if self.type == 'employee':
           if not self.employee:
              raise UserError(_('Employee harus diisi'))

           if not self.roster:
              raise UserError(_('Roster harus diisi'))

           if not self.roster.detail and not self.roster.detail_hari:
              raise UserError(_('Detail Jam Kerja pada Roster harus diisi'))

           else:
              self.env.cr.execute("delete from tbl_msi_shift_schedule where id_gen = %s", (str(self.id),))
              self.env.cr.execute("delete from tbl_msi_rekap_attendance where id_gen = %s", (str(self.id),))

              #self.env.cr.execute("delete from tbl_msi_rekap_attendance where id_gen = %s", (str(self.id),))

              # for emp in self:
                  #self.env.cr.execute("select * from tbl_msi_rekap_attendance where sc_date_a = %s and employee = %s", (self.periode.date_awal, emp.employee.id))
                  #item = self.env.cr.fetchall()
                  #if item:
              self.env.cr.execute("delete from tbl_msi_rekap_attendance where sc_date_a >= %s and employee = %s", (self.periode.date_awal, self.employee.id))
                 # self.env.cr.execute("INSERT into tbl_msi_shift_schedule (id_gen, employee, name, dept, divisi, loc, periode) values (%s,%s,%s,%s,%s,%s,%s)",(self.id, emp.employee.id, emp.employee.nik, emp.employee.department_id.id, emp.employee.divisi.id, emp.employee.lokasi.id, self.periode.id))

              self.env.cr.execute("INSERT into tbl_msi_shift_schedule (id_gen, employee, name, periode) values (%s,%s,%s,%s)",(self.id, self.employee.id, self.employee.nik, self.periode.id))

              kerja=''
              loop_start=0
              loop_jam=-1
              skrg=0
              sc_hadir=''
              nama_hari=''
              c=date.today().day
              b=date.today().month
              a=date.today().year
              d=a+b+c

                  #raise UserError(_('loop start :%s periode loop :%s') % (loop_start, loop_periode))
              while loop_start <= loop_periode :
                    id_roster = self.roster.id + d
                    if self.roster.reguler == False:
                      for emp_sc in self.roster.detail:                         
                        loop_start += 1
                        loop_jam += 1
 
                        jam_awal = get_time_from_float(emp_sc.name.jam_in)
                        jam_akhir = get_time_from_float(emp_sc.name.jam_out)
                        tgl_awal = self.periode.date_awal + timedelta(days=int(loop_jam))
                        if tgl_awal <= year_end:
                          sc_in = (datetime.combine(tgl_awal,jam_awal)) - timedelta(hours=7),

                          if emp_sc.name.overnight:                          
                             sc_out = (datetime.combine((tgl_awal + timedelta(days=1)),jam_akhir)) - timedelta(hours=7),
                          else:                          
                             sc_out = (datetime.combine(tgl_awal,jam_akhir)) - timedelta(hours=7),
                          
                          if str(emp_sc.name.name) == 'OFF' or str(emp_sc.name.name) == 'Off':
                            sc_hadir = 'tdk_hadir'
                            kerja = 'libur'
                          else:
                            sc_hadir = 'hadir'
                            kerja = 'kerja'
                          skrg = tgl_awal.weekday()
                             
                          self.env.cr.execute("INSERT into tbl_msi_rekap_attendance (id_day, id_roster,id_gen, employee, name, periode, sc_name, sc_date_in, sc_date_out, toleransi, max_late, max_early, \
                                                                          sc_hadir, nama_hari, durasi_kerja, jad_lembur, sc_date_a ) \
                                                                          values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)\
                                                                         ",(emp_sc.siklus, id_roster,self.id, self.employee.id, self.employee.nik, self.periode.id, emp_sc.name.id, sc_in, sc_out, emp_sc.name.tol_terlambat, emp_sc.name.max_lama_terlambat, emp_sc.name.min_lama_cepat_pulang, sc_hadir, nama_hari, emp_sc.name.durasi, emp_sc.name.overtime, tgl_awal))

                    if self.roster.reguler == True:
                      # raise UserError(_('Reguler True'))
                      #for emp_hr in self.roster.detail_hari:                         
                        loop_start += 1
                        loop_jam += 1
 
                        tgl_awal = self.periode.date_awal + timedelta(days=int(loop_jam))
                        if tgl_awal <= year_end:
                          skrg = tgl_awal.weekday()
                          cek_hari = self.env['tbl_msi_shift_detail_hari'].sudo().search([('details', '=', self.roster.id),('name', '=', str(skrg))], limit = 1)
                          if cek_hari:
                             jam_awal_0 = str(timedelta(hours=cek_hari.jam_kerja.jam_in))
                             jam_awal = datetime.strptime(jam_awal_0, TIME_FORMAT).time()
                             jam_akhir_0 = str(timedelta(hours=cek_hari.jam_kerja.jam_out))
                             jam_akhir = datetime.strptime(jam_akhir_0, TIME_FORMAT).time()

                             sc_in = (datetime.combine(tgl_awal,jam_awal)) - timedelta(hours=7),
                             #raise UserError(_(jam_awal3))

                             if cek_hari.jam_kerja.overnight:                          
                                sc_out = (datetime.combine((tgl_awal + timedelta(days=1)),jam_akhir)) - timedelta(hours=7),
                             else:                          
                                sc_out = (datetime.combine(tgl_awal,jam_akhir)) - timedelta(hours=7),
                          
                             if str(cek_hari.jam_kerja.name) == 'OFF' or str(cek_hari.jam_kerja.name) == 'Off':
                                 sc_hadir = 'tdk_hadir'
                                 kerja = 'libur'
                             else:
                                 sc_hadir = 'hadir'
                                 kerja = 'kerja'
                             
                             self.env.cr.execute("INSERT into tbl_msi_rekap_attendance (id_gen, employee, name, periode, sc_name, sc_date_in, sc_date_out, toleransi, max_late, max_early, \
                                                                          sc_hadir, nama_hari, durasi_kerja, jad_lembur, sc_date_a ) \
                                                                          values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)\
                                                                         ",(self.id, self.employee.id, self.employee.nik, self.periode.id, cek_hari.jam_kerja.id, sc_in, sc_out, cek_hari.jam_kerja.tol_terlambat, cek_hari.jam_kerja.max_lama_terlambat, cek_hari.jam_kerja.min_lama_cepat_pulang, sc_hadir, nama_hari, cek_hari.jam_kerja.durasi, cek_hari.jam_kerja.overtime, tgl_awal))

                    id_roster = id_roster + 1                             


class tbl_gen_jadual_group(models.Model):
    _name = 'tbl_gen_jadual_group'
    _description = "tbl_gen_jadual_group"

    details = fields.Many2one('tbl_msi_shift_gen_schedule','Details')
    name = fields.Many2one('tbl_msi_employee_group','Name', required=True)
    jml = fields.Float('Jml',default=1)




class tbl_gen_jadual_jam_kerja(models.Model):
    _name = 'tbl_gen_jadual_jam_kerja'
    _description = "tbl_gen_jadual_jam_kerja"

    details = fields.Many2one('tbl_msi_shift_gen_schedule','Details')
    name = fields.Many2one('tbl_msi_jam_kerja','Name', required=True)
    jml = fields.Float('Jml',default=1)
