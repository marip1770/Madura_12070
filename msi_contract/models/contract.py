# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class msi_hr_contract(models.Model):
    _inherit = 'hr.contract'

    u_transport_hdr = fields.Boolean('Transport Per Hadir')
    u_makan_hdr = fields.Boolean('Uang Makan Per Hadir')
    u_kehadiran_hdr = fields.Boolean('Kehadiran Per Hadir')
    u_saku_hdr = fields.Boolean('Uang Saku Per Hadir')
    u_medium_hdr = fields.Boolean('Tunjangan Unit(PAB) Per Hadir')
    u_field_hdr = fields.Boolean('Field Per Hadir')

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
    # u_kinerja = fields.Float('Tunjangan Kinerja')
    u_tanggung_jawab = fields.Float('Tunjangan Tanggung Jawab')
    uang_makan = fields.Float('Uang Makan')
    pot_uang_makan = fields.Float('Uang Makan')
    tunj_tetap = fields.Float('Tunjangan Tetap')

    bpjs_kesehatan = fields.Many2one('tbl_contract_bpjs_kesehatan','BPJS Kesehatan', help='BPJS Kesehatan')
    jp = fields.Many2one('tbl_contract_bpjs_jp','JP', help='BPJS Tenaga Kerja - Jaminan Pensiun')
    jkm = fields.Many2one('tbl_contract_bpjs_jkm','JKM', help='BPJS Tenaga Kerja -  Jaminan Kematian')
    jkk = fields.Many2one('tbl_contract_bpjs_jkk','JKK', help='BPJS Tenaga Kerja -  Jaminan Kecelakaan Kerja')
    jht = fields.Many2one('tbl_contract_bpjs_jht','JHT', help='BPJS Tenaga Kerja -  Jaminan Hari Tua')

    ptkp = fields.Many2one('tbl_employee_ptkp','PTKP', help='Kategori PTKP', related='employee_id.ptkp')

    mata_uang_id = fields.Many2one("res.currency", string="Currency", required=True)
    struktur_gaji = fields.Many2one("tbl_msi_hr_structure", string="Strukture Gaji", required=True)
    akses = fields.Selection([
        ('Direksi', 'Direksi'),
        ('GM', 'GM'),
        ('MGR', 'Manager'),
        ('STAFF', 'Staff'),
        ], string='Akses', default='STAFF')
    akses_ids = fields.Many2one('res.users','Detail')


    gol_gaji = fields.Char('Golongan Gaji')
    analytic_id = fields.Many2one('account.analytic.account', string='Cost Center')

    u_terlambat_hdr = fields.Boolean('Terlambat Per Hadir', default=True)
    u_terlambat = fields.Float('Terlambat')

    nama_tunjangan = fields.Selection([
        ('pkwt', 'PKWT'),
        ('pkwtt', 'PKWTT'),
        ('intern', 'Internship'),
    ], string='Nama Tunjangan & Potongan')
    tipe_tunjangan = fields.Selection([
        ('allowance', 'Allowance'),
        ('deduction', 'Deduction'),
    ], string='Tipe')
    kategori_pendapatan = fields.Selection([
        ('irregular', 'Irregular'),
        ('regular', 'Regular'),
    ], string='Kategori Pendapatan')
    taxable = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Taxable')

    job_lokasi = fields.Many2one('tbl_employee_lokasi', 'Job Lokasi')

    @api.onchange('employee_id')
    def _onchange_employee_id1(self):
        if self.employee_id:
            self.date_start = self.employee_id.tgl_mulai