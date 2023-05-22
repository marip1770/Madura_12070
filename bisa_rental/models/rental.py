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

# class tbl_ops_rental(models.Model):
#     _name = 'tbl_ops_rental'
#     _order = 'name desc'

   
#     tanggal = fields.Date('Tanggal', track_visibility='onchange', default=fields.Date.today())
#     user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user, readonly=True)
#     name = fields.Many2one('hr.employee','Employee', track_visibility='onchange')

class TblRentalKontrak(models.Model):
    _name = 'tbl_bisa_rental_kontrak'
    _rec_name = 'nomor'
    
    nomor = fields.Char('Nomor')
    vendor = fields.Many2one('res.partner', 'Vendor')
    # lokasi = fields.Char('Lokasi')
    tgl_awal = fields.Date('Tanggal Awal')
    tgl_akhir = fields.Date('Tanggal Akhir')
    no_projek = fields.Many2one('project.project', 'No Project')
    produk = fields.Many2one('product.product', 'Produk')
    lokasi = fields.Many2one('tbl_bisa_kontrak_lokasi', 'Lokasi')
    quantity = fields.Integer('QTY')
    harga = fields.Integer('Harga')
    total = fields.Integer('Total')
    nilai_kontrak = fields.Integer('Nilai Kontrak')
    # detailkontrak = fields.Many2one('tbl_bisa_hauling_kontrak', 'Detail Kontrak')
    # detail_kontrak = fields.One2many('tbl_bisa_hauling_detail_kontrak', 'detailkontrak', 'detail kontrak')

# class TblHaulingDetailKontrak(models.Model):
#     _name = 'tbl_bisa_hauling_detail_kontrak'
    
#     produk = fields.Many2one('product.product', 'Produk')
#     lokasi = fields.Many2one('res.partner', 'Lokasi')
#     quantity = fields.Integer('QTY')
#     harga = fields.Integer('Harga')
#     total = fields.Integer('Total')
#     detailkontrak = fields.Many2one('tbl_bisa_hauling_kontrak', 'Detail Kontrak')

class TblRentalPlan(models.Model):
    _name = 'tbl_bisa_rental_plan'

class TblRentalAssigment(models.Model):
    _name = 'tbl_bisa_rental_assigment'

class TblRentalP5m(models.Model):
    _name = 'tbl_bisa_rental_p5m'
    _rec_name = 'nomor'

    nomor = fields.Char('Nomor', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    tgl_terbit = fields.Date('Tanggal Terbit', default=fields.Date.today())
    revisi = fields.Integer('Revisi')
    tanggal = fields.Date('Tanggal')
    # departemen = fields.Char('Departemen')
    departemen = fields.Many2one('hr.department','Departemen')
    lokasi = fields.Char('Lokasi')
    pemateri = fields.Char('Pemberi Materi')
    jml_peserta = fields.Integer('Jumlah Peserta')
    pertanyaan = fields.One2many('tbl_bisa_rental_p5m_quest', 'quest', 'Pertanyaan')
    data1 = fields.One2many('tbl_bisa_rental_absensi_p5m', 'data', 'data')

    @api.model
    def create(self, vals):
        if vals.get('nomor', _('New')) == _('New'):
            vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p5m') or _('New')
        result = super(TblRentalP5m, self).create(vals)
        return result

class TblRentalP5mQuest(models.Model):
    _name = 'tbl_bisa_rental_p5m_quest'

    tanya = fields.Text('Materi Pembahasan Dalam Pengarahan Harian, Sebagai Berikut')
    quest = fields.Many2one('tbl_bisa_rental_p5m', 'Quest')

class TblRentalAbsensi(models.Model):
    _name = 'tbl_bisa_rental_absensi_p5m'

    sn = fields.Integer('SN')
    nama = fields.Char('Nama')
    # Departemen = fields.Char('Departemen')
    Departemen = fields.Many2one('hr.department','Departemen') 
    tanda_tangan = fields.Char('Tanda Tangan')
    data = fields.Many2one('tbl_bisa_rental_p5m', 'Data')

class TblRentalP2h(models.Model):
    _name = 'tbl_bisa_rental_p2h'
    _rec_name = 'nomor'

    nomor = fields.Char('Nomor', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    tgl_terbit = fields.Date('Tanggal Terbit', default=fields.Date.today())
    revisi = fields.Integer('Revisi')
    data2 = fields.One2many('tbl_bisa_rental_data_p2h', 'data', 'dataa')

    @api.model
    def create(self, vals):
        if vals.get('nomor', _('New')) == _('New'):
            vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p2h') or _('New')
        result = super(TblRentalP2h, self).create(vals)
        return result

class TblRentalDataP2h(models.Model):
    _name = 'tbl_bisa_rental_data_p2h'

    data = fields.Many2one('tbl_bisa_p5m', 'Data P2h')
    nama = fields.Char('Nama')
    sn = fields.Integer('SN')
    jabatan = fields.Char('Jabatan/Departemen/Perusahaan')
    tidur_jam = fields.Float('Tidur Dari Jam')
    bangun_jam = fields.Float('Bangun Jam')
    total_istirahat = fields.Float('Total Istirahat')
    tanda_tangan = fields.Char('Tanda Tangan')

class TblRentalTimeSheet(models.Model):
    _name = 'tbl_bisa_rental_time_sheet'

    driver_name = fields.Char('Operation/Driver Name')
    tanggal = fields.Date('Date')
    shift = fields.Selection([
        ('siang', 'Siang'), 
        ('malam', 'Malam'), 
    ], 'Shift')
    work_location = fields.Char('Work Location')
    code_unit = fields.Char('Code Unit')
    kind_of_equipment = fields.Char('Kind of Equipment')
    operation_hours = fields.Char('Operation Hours')
    operation_hours_meter = fields.Char('Operation Hours Meter')
    job_description = fields.Char('Job Description')
    ritase = fields.Char('Ritase')
    fuel = fields.Char('Fuel(Liter)')