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

# class tbl_ops_port(models.Model):
#     _name = 'tbl_ops_port'
#     _order = 'name desc'

   
#     tanggal = fields.Date('Tanggal', track_visibility='onchange', default=fields.Date.today())
#     user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user, readonly=True)
#     name = fields.Many2one('hr.employee','Employee', track_visibility='onchange')

class TblPortKontrak(models.Model):
    _name = 'tbl_bisa_port_kontrak'
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

class TblPortPlan(models.Model):
    _name = 'tbl_bisa_port_plan'

class TblPortAssigment(models.Model):
    _name = 'tbl_bisa_port_assigment'

class TblPortP5m(models.Model):
    _name = 'tbl_bisa_port_p5m'
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
    pertanyaan = fields.One2many('tbl_bisa_p5m_quest', 'quest', 'Pertanyaan')
    data1 = fields.One2many('tbl_bisa_port_absensi_p5m', 'data', 'data')

    @api.model
    def create(self, vals):
        if vals.get('nomor', _('New')) == _('New'):
            vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p5m') or _('New')
        result = super(TblPortP5m, self).create(vals)
        return result


class TblPortP5mQuest(models.Model):
    _name = 'tbl_bisa_port_p5m_quest'

    tanya = fields.Text('Materi Pembahasan Dalam Pengarahan Harian, Sebagai Berikut')
    quest = fields.Many2one('tbl_bisa_port_p5m', 'Quest')

class TblPortAbsensi(models.Model):
    _name = 'tbl_bisa_port_absensi_p5m'

    sn = fields.Integer('SN')
    nama = fields.Char('Nama')
    # Departemen = fields.Char('Departemen')
    Departemen = fields.Many2one('hr.department','Departemen')
    tanda_tangan = fields.Char('Tanda Tangan')
    data = fields.Many2one('tbl_bisa_port_p5m', 'Data')

class TblPortP2h(models.Model):
    _name = 'tbl_bisa_port_p2h'
    _rec_name = 'nomor'

    nomor = fields.Char('Nomor', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    tgl_terbit = fields.Date('Tanggal Terbit', default=fields.Date.today())
    revisi = fields.Integer('Revisi')
    data2 = fields.One2many('tbl_bisa_port_data_p2h', 'data', 'dataa')

    @api.model
    def create(self, vals):
        if vals.get('nomor', _('New')) == _('New'):
            vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p2h') or _('New')
        result = super(TblPortP2h, self).create(vals)
        return result

class TblPortDataP2h(models.Model):
    _name = 'tbl_bisa_port_data_p2h'

    data = fields.Many2one('tbl_bisa_port_p2h', 'Data P2h')
    nama = fields.Char('Nama')
    sn = fields.Integer('SN')
    jabatan = fields.Char('Jabatan/Departemen/Perusahaan')
    tidur_jam = fields.Float('Tidur Dari Jam')
    bangun_jam = fields.Float('Bangun Jam')
    total_istirahat = fields.Float('Total Istirahat')
    tanda_tangan = fields.Char('Tanda Tangan')

class TblPortWorkRequest(models.Model):
    _name = 'tbl_bisa_port_work_request'

    nomor = fields.Char('Nomor', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    tgl_terbit = fields.Date('Tanggal Terbit', default=fields.Date.today())
    revisi = fields.Integer('Revisi')
    tanggal = fields.Date('Date/Tanggal')
    shift = fields.Selection([
        ('siang', 'Siang'), 
        ('malam', 'Malam'), 
    ], 'Shift')
    maintenance_type = fields.Selection([
        ('repair_bd', 'Repair (B/D)'), 
        ('overhoul_oh', 'Overhoul (OH)'), 
        ('accident_acd', 'Accident (ACD)'),
    ], 'Maintenance Type')
    unit_id = fields.Char('Unit ID')
    operator_driver = fields.Char('Operator/Drive')
    hm_km = fields.Char('HM/KM')
    model = fields.Char('Model')
    time_start = fields.Float('Time Start/Jam Masuk')
    time_stop = fields.Float('Time Stop/Jam Keluar')
    status = fields.Selection([
        ('ready', 'Ready'), 
        ('continue', 'Continue'), 
    ], 'Status')
    joline = fields.One2many('tbl_bisa_port_job_out_line', 'data_joline', 'Jo Line')
    maline = fields.One2many('tbl_bisa_port_mecanic_action_line', 'data_maline', 'Ma Line')

    @api.model
    def create(self, vals):
        if vals.get('nomor', _('New')) == _('New'):
            vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_work_req') or _('New')
        result = super(TblPortWorkRequest, self).create(vals)
        return result

class TblPortJobOutLine(models.Model):
    _name = 'tbl_bisa_port_job_out_line'

    job_out_line = fields.Char('Job Out Line/Jenis Kerusakan')
    data_joline = fields.Many2one('tbl_bisa_port_work_request', 'Data Job Out Line')

class TblPortMecanicActionLine(models.Model):
    _name = 'tbl_bisa_port_mecanic_action_line'

    mecanic_action = fields.Char('Mecanic Action Taken/Pekerjaan Mekanik')
    time_progress_start = fields.Float('Start')
    time_progress_stop = fields.Float('Stop')
    time_progress_total = fields.Float('Total')
    mechanic_name = fields.Char('Mechanic Name')
    data_maline = fields.Many2one('tbl_bisa_port_work_request', 'Data Mechanic Line')

class TBlPortWorkRequestDepartment(models.Model):
    _name = 'tbl_bisa_port_work_request_dept'

    nomor = fields.Char('Nomor', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    departement = fields.Char('Departemen')
    number = fields.Char('Number')
    hari = fields.Char('Hari/Day')
    tanggal = fields.Date('Tanggal/Date')
    detail = fields.One2many('tbl_bisa_port_detail_wrd', 'data', 'Detail')

    @api.model
    def create(self, vals):
        if vals.get('nomor', _('New')) == _('New'):
            vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_work_req_dept') or _('New')
        result = super(TBlWorkRequestDepartment, self).create(vals)
        return result

class TblPortDetailWrd(models.Model):
    _name = 'tbl_bisa_port_detail_wrd'
    
    description = fields.Char('Description')
    qty = fields.Integer('QTY')
    uom = fields.Char('UOM')
    remark = fields.Char('Remark')
    data = fields.Many2one('tbl_bisa_work_request_dept', 'Data')
