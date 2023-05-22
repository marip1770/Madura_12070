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

class tbl_hr_tipe_mutasi(models.Model):
    _name = 'tbl_hr_tipe_mutasi'
    _order = 'name'

    name = fields.Char('Name')

class tbl_hr_mutasi(models.Model):
    _name = 'tbl_hr_mutasi'
    _order = 'tanggal desc'

   
    tanggal = fields.Date('Tanggal', track_visibility='onchange', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user, readonly=True)

    name = fields.Many2one('hr.employee','Employee', track_visibility='onchange')
    nik = fields.Char('NIK', track_visibility='onchange')
    tipe = fields.Many2one('tbl_hr_tipe_mutasi','Tipe', track_visibility='onchange')
    desc = fields.Text('Deskripsi', track_visibility='onchange')
    tindak_lanjut = fields.Text('Tindak Lanjut', track_visibility='onchange')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')


    divisi = fields.Many2one('tbl_employee_divisi','Divisi')
    lokasi = fields.Many2one('tbl_employee_lokasi','Lokasi')
    job_id = fields.Many2one('hr.job', 'Job Position')
    department_id = fields.Many2one('hr.department', 'Department')
    wage = fields.Float('Gaji Pokok')
    u_transport = fields.Float('Transport')
    u_makan = fields.Float('Uang Makan')
    u_kehadiran = fields.Float('Kehadiran')
    u_komunikasi = fields.Float('Komunikasi')
    u_perumahan = fields.Float('Perumahan')
    u_keluarga = fields.Float('Keluarga')
    u_daerah = fields.Float('Penempatan Daerah')
    u_jabatan = fields.Float('Jabatan')
    u_keahlian = fields.Float('Keahlian')
    u_khusus = fields.Float('Khusus')
    u_hari_tua = fields.Float('Hari Tua')
    u_field = fields.Float('Field')
    u_saku = fields.Float('Uang Saku')
    u_kebersihan = fields.Float('Kebersihan Unit')
    u_medium = fields.Float('Tunjangan Unit(PAB)')
    u_hd = fields.Float('Tunjangan Unit(HD)')
    u_se = fields.Float('Tunjangan Unit(SE)')
    u_kinerja = fields.Float('Tunjangan Kinerja')
    u_tanggung_jawab = fields.Float('Tunjangan Tanggung Jawab')
    struktur_gaji = fields.Many2one("tbl_msi_hr_structure", string="Strukture Gaji")
    gol_gaji = fields.Char('Golongan Gaji')
    analytic_id = fields.Many2one('account.analytic.account', string='Cost Center')

    is_divisi = fields.Boolean('Divisi')
    is_lokasi = fields.Boolean('Lokasi')
    is_job_id = fields.Boolean('Job Position')
    is_department_id = fields.Boolean( 'Department')
    is_wage = fields.Boolean( 'Gaji Pokok')
    is_u_transport = fields.Boolean('Transport')
    is_u_makan = fields.Boolean('Uang Makan')
    is_u_kehadiran = fields.Boolean('Kehadiran')
    is_u_komunikasi = fields.Boolean('Komunikasi')
    is_u_perumahan = fields.Boolean('Perumahan')
    is_u_keluarga = fields.Boolean('Keluarga')
    is_u_daerah = fields.Boolean('Penempatan Daerah')
    is_u_jabatan = fields.Boolean('Jabatan')
    is_u_keahlian = fields.Boolean('Keahlian')
    is_u_khusus = fields.Boolean('Khusus')
    is_u_hari_tua = fields.Boolean('Hari Tua')
    is_u_field = fields.Boolean('Field')
    is_u_saku = fields.Boolean('Uang Saku')
    is_u_kebersihan = fields.Boolean('Kebersihan Unit')
    is_u_medium = fields.Boolean('Tunjangan Unit(PAB)')
    is_u_hd = fields.Boolean('Tunjangan Unit(HD)')
    is_u_se = fields.Boolean('Tunjangan Unit(SE)')
    is_u_kinerja = fields.Boolean('Tunjangan Kinerja')
    is_u_tanggung_jawab = fields.Boolean('Tunjangan Tanggung Jawab')
    is_struktur_gaji = fields.Boolean( required=True)
    is_gol_gaji = fields.Boolean('Golongan Gaji')
    is_analytic_id = fields.Boolean('Cost Center')

    new_divisi = fields.Many2one('tbl_employee_divisi','Divisi')
    new_lokasi = fields.Many2one('tbl_employee_lokasi','Lokasi')
    new_job_id = fields.Many2one('hr.job', 'Job Position')
    new_department_id = fields.Many2one('hr.department', 'Department')
    new_wage = fields.Float('Gaji Pokok')
    new_u_transport = fields.Float('Transport')
    new_u_makan = fields.Float('Uang Makan')
    new_u_kehadiran = fields.Float('Kehadiran')
    new_u_komunikasi = fields.Float('Komunikasi')
    new_u_perumahan = fields.Float('Perumahan')
    new_u_keluarga = fields.Float('Keluarga')
    new_u_daerah = fields.Float('Penempatan Daerah')
    new_u_jabatan = fields.Float('Jabatan')
    new_u_keahlian = fields.Float('Keahlian')
    new_u_khusus = fields.Float('Khusus')
    new_u_hari_tua = fields.Float('Hari Tua')
    new_u_field = fields.Float('Field')
    new_u_saku = fields.Float('Uang Saku')
    new_u_kebersihan = fields.Float('Kebersihan Unit')
    new_u_medium = fields.Float('Tunjangan Unit(PAB)')
    new_u_hd = fields.Float('Tunjangan Unit(HD)')
    new_u_se = fields.Float('Tunjangan Unit(SE)')
    new_u_kinerja = fields.Float('Tunjangan Kinerja')
    new_u_tanggung_jawab = fields.Float('Tunjangan Tanggung Jawab')
    new_struktur_gaji = fields.Many2one("tbl_msi_hr_structure", string="Strukture Gaji")
    new_gol_gaji = fields.Char('Golongan Gaji')
    new_analytic_id = fields.Many2one('account.analytic.account', string='Cost Center')

    @api.onchange('name')
    def _compute_name(self):
        if self.name:
            self.nik = self.name.nik
            self.divisi = self.name.divisi.id
            self.lokasi = self.name.lokasi.id
            self.job_id = self.name.job_id.id
            self.department_id = self.name.department_id.id
            self.new_divisi = self.name.divisi.id
            self.new_lokasi = self.name.lokasi.id
            self.new_job_id = self.name.job_id.id
            self.new_department_id = self.name.department_id.id

            kontrak = self.env['hr.contract'].search([('employee_id', '=', self.name.id)], limit=1, order='id desc')
            if kontrak:
                self.wage = kontrak.wage
                self.u_transport = kontrak.u_transport
                self.u_makan = kontrak.u_makan
                self.u_kehadiran = kontrak.u_kehadiran
                self.u_komunikasi = kontrak.u_komunikasi
                self.u_perumahan = kontrak.u_perumahan
                self.u_keluarga = kontrak.u_keluarga
                self.u_daerah = kontrak.u_daerah
                self.u_jabatan = kontrak.u_jabatan
                self.u_keahlian = kontrak.u_keahlian
                self.u_khusus = kontrak.u_khusus
                self.u_hari_tua = kontrak.u_hari_tua
                self.u_field = kontrak.u_field
                self.u_saku = kontrak.u_saku
                self.u_kebersihan = kontrak.u_kebersihan
                self.u_medium = kontrak.u_medium
                self.u_hd = kontrak.u_hd
                self.u_se = kontrak.u_se
                self.u_kinerja = kontrak.u_kinerja
                self.u_tanggung_jawab = kontrak.u_tanggung_jawab
                self.struktur_gaji = kontrak.struktur_gaji
                self.gol_gaji = kontrak.gol_gaji
                self.analytic_id = kontrak.analytic_id
                
                self.new_wage = kontrak.wage
                self.new_u_transport = kontrak.u_transport
                self.new_u_makan = kontrak.u_makan
                self.new_u_kehadiran = kontrak.u_kehadiran
                self.new_u_komunikasi = kontrak.u_komunikasi
                self.new_u_perumahan = kontrak.u_perumahan
                self.new_u_keluarga = kontrak.u_keluarga
                self.new_u_daerah = kontrak.u_daerah
                self.new_u_jabatan = kontrak.u_jabatan
                self.new_u_keahlian = kontrak.u_keahlian
                self.new_u_khusus = kontrak.u_khusus
                self.new_u_hari_tua = kontrak.u_hari_tua
                self.new_u_field = kontrak.u_field
                self.new_u_saku = kontrak.u_saku
                self.new_u_kebersihan = kontrak.u_kebersihan
                self.new_u_medium = kontrak.u_medium
                self.new_u_hd = kontrak.u_hd
                self.new_u_se = kontrak.u_se
                self.new_u_kinerja = kontrak.u_kinerja
                self.new_u_tanggung_jawab = kontrak.u_tanggung_jawab
                self.new_struktur_gaji = kontrak.struktur_gaji
                self.new_gol_gaji = kontrak.gol_gaji
                self.new_analytic_id = kontrak.analytic_id