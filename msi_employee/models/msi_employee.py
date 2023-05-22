# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime, date, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare


class msi_hr_employee(models.Model):
    _inherit = 'hr.employee'

    # nik = fields.Char('NIK', default='New', track_visibility='onchange')
    certificate = fields.Selection([
        ('sd', 'SD'),
        ('smp', 'Bachelor'),
        ('sma_smk', 'SMA / SMK'),
        ('diploma', 'Diploma'),
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('other', 'Other'),
    ], 'Certificate Level', default='master', groups="hr.group_hr_user")
    nik = fields.Char('NIK', default='New')
    new_nik = fields.Char('NIK', default='New')
    is_create = fields.Boolean('Is Create')
    personal_email = fields.Char('Personal Email', track_visibility='onchange')
    sent_email = fields.Boolean('Sent Payslip Email', track_visibility='onchange')
    nama_depan = fields.Char('Nama Depan', track_visibility='onchange')
    nama_tengah = fields.Char('Nama Tengah')
    nama_belakang = fields.Char('Nama Belakang', track_visibility='onchange')
    agama = fields.Selection([
        ('islam', 'Islam'),
        ('kristen_katolik', 'Kristen Katolik'),
        ('kristen_protestan', 'Kristen Protestan'),
        ('hindu', 'Hindu'),
        ('budha', 'Budha'),
        ('kepercayaan', 'Kepercayaan'),
        ('lainnya', 'Lainnya'),
    ], string="Agama",default='lainnya', track_visibility='onchange',)
    darah = fields.Selection([
        ('o', 'O'),
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
    ], string="Gol Darah",default='o', track_visibility='onchange',)
    job_grading = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
    ], string="Job Grading",default='1', track_visibility='onchange')
    no_hp = fields.Char('No Hp', track_visibility='onchange')
    no_ktp = fields.Char('No KTP', track_visibility='onchange')
    no_kk = fields.Char('No KK', track_visibility='onchange')
    no_npwp = fields.Char('No NPWP', track_visibility='onchange')
    no_bpjs_tenagakerja = fields.Char('BPJS Ketenagakerjaan', track_visibility='onchange')
    no_bpjs_kesehatan = fields.Char('BPJS Kesehatan', track_visibility='onchange')

    ptkp = fields.Many2one('tbl_employee_ptkp','PTKP', track_visibility='onchange')
    tanggal_pajak_start = fields.Date('Tanggal Mulai PTKP', track_visibility='onchange')
    tanggal_pajak_akhir = fields.Date('Tanggal Berakhir', track_visibility='onchange')

    darurat_kontak = fields.Char('Kontak Darurat', track_visibility='onchange')
    darurat_alamat = fields.Char('Alamat Darurat', track_visibility='onchange')
    darurat_telp = fields.Char('Telp Darurat', track_visibility='onchange')
    detail_family = fields.One2many('tbl_employee_family','details','Family Detail', track_visibility='onchange')
    detail_education = fields.One2many('tbl_employee_education','details','Education Detail', track_visibility='onchange')

    divisi = fields.Many2one('tbl_employee_divisi','Divisi', track_visibility='onchange')
    lokasi = fields.Many2one('tbl_employee_lokasi','Lokasi', track_visibility='onchange')

    tgl_mulai = fields.Date('Mulai Kerja', track_visibility='onchange')
    tgl_selesai = fields.Date('Tanggal Berhenti', track_visibility='onchange')
    is_exit = fields.Boolean('Berhenti Kerja', default=False, track_visibility='onchange')

    nama_bank = fields.Char('Nama Bank', track_visibility='onchange')
    no_rekening = fields.Char('No Rekening', track_visibility='onchange')
    nama_rekening = fields.Char('Nama Rekening', track_visibility='onchange')

    npwp = fields.Boolean('NPWP', track_visibility='onchange')
    no_npwp = fields.Char('Nomor NPWP', track_visibility='onchange')

    gross = fields.Boolean('Is Gross UP', track_visibility='onchange')

    detail_work_experience = fields.One2many('tbl_employee_work_experience','details','Work Experience', track_visibility='onchange')
    detail_bahasa = fields.One2many('tbl_employee_bahasa','details','Bahasa', track_visibility='onchange')

    detail_sertifikat = fields.One2many('tbl_employee_sertifikat','details','Sertifikat Detail', track_visibility='onchange')
    detail_training = fields.One2many('tbl_employee_training','details','Training Detail', track_visibility='onchange')
    detail_dokumen = fields.One2many('tbl_employee_dokumen', 'details','Dokumen Detail', track_visibility='onchange')

    coach_id = fields.Many2one('hr.employee', 'Atasan Langsung', track_visibility='onchange')

    lokasi_gudang = fields.Many2one('stock.warehouse','Lokasi Gudang', track_visibility='onchange')

    latihan_pengalaman_kerja = fields.Text('Latihan & Pengalaman Kerja Lain', track_visibility='onchange')
    

    wajib_kerja = fields.Boolean('Pernah Melakukan Wajib Kerja', default=False, track_visibility='onchange')
    detail_wajib_kerja = fields.One2many('tbl_employee_wajib_kerja', 'details','Wajib Kerja Detail', track_visibility='onchange')
    keahlian_khusus_wajib_kerja = fields.Text('Keahlian Khusus Selama Wajib Kerja', track_visibility='onchange')
    detail_kegiatan_organisasi = fields.One2many('tbl_employee_kegiatan_organisasi', 'details','Kegiatan Organisasi', track_visibility='onchange')
    kegemaran = fields.Text('Kegemaran', track_visibility='onchange')
    pernah_melamar_malindo = fields.Boolean('Pernah Melamar kerja di Malindo', default=False, track_visibility='onchange')
    saudara_malindo = fields.Boolean('Ada Saudara di Malindo', default=False, track_visibility='onchange')
    terlibat_kriminal = fields.Boolean('Pernah Terlibat Kriminal', default=False, track_visibility='onchange')
    detail_referensi = fields.One2many('tbl_employee_referensi', 'details','Referensi', track_visibility='onchange')

    alamat_surat = fields.Text('Alamat Surat', track_visibility='onchange')
    no_akte = fields.Char('No Akte Kelahiran', track_visibility='onchange')
    no_sim = fields.Char('No SIM', track_visibility='onchange')
    tinggi = fields.Char('Tinggi (cm)', track_visibility='onchange')
    berat = fields.Char('Berat (kg)', track_visibility='onchange')
    cacat = fields.Char('Cacat Tubuh', track_visibility='onchange')
    umur = fields.Float('Age', track_visibility='onchange')
    # @api.model
    # def create(self, vals):
    #     if vals.get('nik', _('New')) == _('New'):
    #        vals['nik'] = self.env['ir.sequence'].next_by_code('nik')
    #     result = super(msi_hr_employee, self).create(vals)
    #     return result

    def create_nik(self):
        departemen = str(self.department_id.kode_department)
        lokasi = str(self.lokasi.kode_lokasi)
        str_thn = str(self.tgl_mulai)[2:4]
        self.nik = lokasi+'.'+departemen+'.'+str_thn+'.'+self.env['ir.sequence'].next_by_code('nik')
        self.is_create = True

    @api.onchange('nama_depan','nama_tengah','nama_belakang')
    def _compute_nama_lengkap(self):
        if self.nama_tengah and not self.nama_belakang:
           self.name = str(self.nama_depan).upper() + ' ' + str(self.nama_tengah).upper()
        if self.nama_tengah and self.nama_belakang:
           self.name = str(self.nama_depan).upper() + ' ' + str(self.nama_tengah).upper() + ' ' + str(self.nama_belakang).upper()
        if not self.nama_tengah and self.nama_belakang:
           self.name = str(self.nama_depan).upper() + ' ' + str(self.nama_belakang).upper()
        if self.nama_depan and not self.nama_belakang and not self.nama_tengah:
           self.name = str(self.nama_depan).upper()

    @api.onchange('birthday','tgl_mulai')
    def _compute_usia_masa_kerja(self):
        if self.birthday:
           today = date.today()
           usia = 0
           usia = today.year - self.birthday.year
           # usia = relativedelta(self.birthday, fields.Date.today())
           self.umur = usia

    _sql_constraints = [('nik_unique', 'unique(nik)', 'NIK already exists')]

class tbl_employee_family(models.Model):
    _name = 'tbl_employee_family'

    details = fields.Many2one('hr.employee','Family Detail')
    name = fields.Char('Name')
    tgl_lahir = fields.Date('Tanggal Lahir')
    tempat_lahir = fields.Char('Tempat Lahir')
    hubungan = fields.Char('Hubungan')
    status_pajak = fields.Char('Status Pajak')
    status_pernikahan = fields.Char('Status Pernikahan')
    pekerjaan = fields.Char('Pekerjaan')
    tempat_bekerja = fields.Char('Tempat Bekerja')


class tbl_employee_education(models.Model):
    _name = 'tbl_employee_education'

    details = fields.Many2one('hr.employee','Family Detail')
    name = fields.Char('Nama Institusi')
    tingkat = fields.Char('Jenjang')
    jurusan = fields.Char('Jurusan')
    tahun_mulai = fields.Char('Tahun Mulai')
    tahun_lulus = fields.Char('Tahun Lulus')
    izasah = fields.Char('Izasah')

class tbl_employee_work_experience(models.Model):
    _name = 'tbl_employee_work_experience'

    details = fields.Many2one('hr.employee','Employee')
    name = fields.Char('Nama Perusahaan')
    jabatan = fields.Char('Jabatan')
    nama_atasan = fields.Char('Nama Atasan')
    dari = fields.Date('Dari')
    sampai = fields.Date('Sampai')
    gaji_awal = fields.Float('Gaji Awal')
    gaji_terakhir = fields.Float('Gaji Terakhir')
    alasan_keluar = fields.Char('Alasan Keluar')
    uraian_pekerjaan = fields.Text('Uraian Pekerjaan')

class tbl_employee_bahasa(models.Model):
    _name = 'tbl_employee_bahasa'

    details = fields.Many2one('hr.employee','Employee')
    name = fields.Char('Bahasa')
    bicara = fields.Selection([
        ('baik', 'Baik'),
        ('sedang', 'Sedang'),
        ('kurang', 'Kurang'),
    ], string='Bicara')
    menulis = fields.Selection([
        ('baik', 'Baik'),
        ('sedang', 'Sedang'),
        ('kurang', 'Kurang'),
    ], string='Menulis')
    pemahaman = fields.Selection([
        ('baik', 'Baik'),
        ('sedang', 'Sedang'),
        ('kurang', 'Kurang'),
    ], string='Pemahaman')

class tbl_employee_divisi(models.Model):
    _name = 'tbl_employee_divisi'

    name = fields.Char('Name')

class tbl_employee_lokasi(models.Model):
    _name = 'tbl_employee_lokasi'

    name = fields.Char('Name')
    kode_lokasi = fields.Char('Kode Lokasi')
    project = fields.Many2one('project.project', 'Nama Projek')


class tbl_contract_bpjs_kesehatan(models.Model):
    _name = 'tbl_contract_bpjs_kesehatan'
    _description = "bpjs_kesehatan"

    name = fields.Char('Name')
    karyawan = fields.Float('Ditanggung Karyawan (%)')
    perusahaan = fields.Float('Dibayarkan Perusahaan (%)')


class tbl_contract_bpjs_jp(models.Model):
    _name = 'tbl_contract_bpjs_jp'
    _description = "tbl_contract_bpjs_jp"

    name = fields.Char('Name')
    karyawan = fields.Float('Ditanggung Karyawan (%)')
    perusahaan = fields.Float('Dibayarkan Perusahaan (%)')


class tbl_contract_bpjs_jkm(models.Model):
    _name = 'tbl_contract_bpjs_jkm'
    _description = "tbl_contract_bpjs_jkm"

    name = fields.Char('Name')
    karyawan = fields.Float('Ditanggung Karyawan (%)')
    perusahaan = fields.Float('Dibayarkan Perusahaan (%)')


class tbl_contract_bpjs_jkk(models.Model):
    _name = 'tbl_contract_bpjs_jkk'
    _description = "tbl_contract_bpjs_jkk"

    name = fields.Char('Name')
    karyawan = fields.Float('Ditanggung Karyawan (%)')
    perusahaan = fields.Float('Dibayarkan Perusahaan (%)')


class tbl_contract_bpjs_jht(models.Model):
    _name = 'tbl_contract_bpjs_jht'
    _description = "tbl_contract_bpjs_jht"

    name = fields.Char('Name')
    karyawan = fields.Float('Ditanggung Karyawan (%)')
    perusahaan = fields.Float('Dibayarkan Perusahaan (%)')


class tbl_contract_kategori_pajak(models.Model):
    _name = 'tbl_contract_kategori_pajak'
    _description = "tbl_contract_kategori_pajak"

    name = fields.Char('Name')


class tbl_employee_ptkp(models.Model):
    _name = 'tbl_employee_ptkp'
    _description = "tbl_employee_ptkp"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name')
    value = fields.Float('Value')
    ket = fields.Char('Keterangan')

class tbl_employee_sertifikat(models.Model):
    _name = 'tbl_employee_sertifikat'

    details = fields.Many2one('hr.employee','Sertifikat Detail')
    name = fields.Char('Nama Institusi')
    desc = fields.Char('Deskripsi')
    tipe = fields.Many2one('tbl_emoployee_tipe_training','Tipe')
    tahun = fields.Char('Tahun')

class tbl_employee_training(models.Model):
    _name = 'tbl_employee_training'

    details = fields.Many2one('hr.employee','Training Detail')
    name = fields.Char('Nama Institusi')
    desc = fields.Char('Deskripsi')
    tipe = fields.Many2one('tbl_emoployee_tipe_training','Tipe')
    tahun = fields.Char('Tahun')

class tbl_employee_wajib_kerja(models.Model):
    _name = 'tbl_employee_wajib_kerja'

    details = fields.Many2one('hr.employee','Employee')
    name = fields.Char('Jenis Wajib Kerja')
    tgl_mulai = fields.Date('Tanggal Mulai')
    tgl_selesai = fields.Date('Tanggal Selesai')
    hasil = fields.Char('Hasil')

class tbl_employee_kegiatan_organisasi(models.Model):
    _name = 'tbl_employee_kegiatan_organisasi'

    details = fields.Many2one('hr.employee','Employee')
    name = fields.Char('Nama Organisasi')
    jabatan = fields.Char('Jabatan')
    tahun = fields.Char('Tahun')

class tbl_employee_referensi(models.Model):
    _name = 'tbl_employee_referensi'

    details = fields.Many2one('hr.employee','Employee')
    name = fields.Char('Nama')
    alamat = fields.Char('Alamat')
    no_tel = fields.Char('No. Tel')
    pekerjaan = fields.Char('Pekerjaan')
    lama_kenal = fields.Char('Lama Kenal')

class tbl_emoployee_tipe_training(models.Model):
    _name = 'tbl_emoployee_tipe_training'

    name = fields.Char('Name')

class tbl_employee_dokumen(models.Model):
    _name = 'tbl_employee_dokumen'

    nama_dok = fields.Char('Nama Dokumen')
    ket_doc = fields.Char('Keterangan Dokumen')
    tgl_mulai = fields.Date('Tanggal Mulai')
    tgl_selesai = fields.Date('Tanggal Selesai')
    details = fields.Many2one('hr.employee', 'Dokumen Detail')
