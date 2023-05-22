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

# class tbl_ops_briefing(models.Model):
#     _name = 'tbl_ops_briefing'
#     _order = 'name desc'

   
#     tanggal = fields.Date('Tanggal', track_visibility='onchange', default=fields.Date.today())
#     user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user, readonly=True)
#     name = fields.Many2one('hr.employee','Employee', track_visibility='onchange')

# class TblPlan(models.Model):
#     _name = 'tbl_bisa_plan'

# class TblAssigment(models.Model):
#     _name = 'tbl_bisa_assigment'

class TblP5m(models.Model):
    _name = 'tbl_bisa_p5m'
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
    data1 = fields.One2many('tbl_bisa_absensi_p5m', 'data', 'data')

    # @api.model
    # def create(self, vals):
    #     if vals.get('nomor', _('New')) == _('New'):
    #         vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p5m') or _('New')
    #     result = super(TblP5m, self).create(vals)
    #     return result


class TblP5mQuest(models.Model):
    _name = 'tbl_bisa_p5m_quest'

    tanya = fields.Text('Materi Pembahasan Dalam Pengarahan Harian, Sebagai Berikut')
    quest = fields.Many2one('tbl_bisa_p5m', 'Quest')

class TblAbsensi(models.Model):
    _name = 'tbl_bisa_absensi_p5m'

    sn = fields.Integer('SN')
    nama = fields.Char('Nama')
    # Departemen = fields.Char('Departemen')
    Departemen = fields.Many2one('hr.department','Departemen')
    tanda_tangan = fields.Char('Tanda Tangan')
    data = fields.Many2one('tbl_bisa_p5m', 'Data')

class TblP2h(models.Model):
    _name = 'tbl_bisa_p2h'
    _rec_name = 'nomor'

    nomor = fields.Char('Nomor')
    tgl_terbit = fields.Date('Tanggal Terbit', default=fields.Date.today())
    revisi = fields.Integer('Revisi')
    data2 = fields.One2many('tbl_bisa_data_p2h', 'data', 'dataa')

    # @api.model
    # def create(self, vals):
    #     if vals.get('nomor', _('New')) == _('New'):
    #         vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p2h') or _('New')
    #     result = super(TblP2h, self).create(vals)
    #     return result

class TblDataP2h(models.Model):
    _name = 'tbl_bisa_data_p2h'

    data = fields.Many2one('tbl_bisa_p2h', 'Data P2h')
    nama = fields.Char('Nama')
    sn = fields.Integer('SN')
    jabatan = fields.Char('Jabatan/Departemen/Perusahaan')
    tidur_jam = fields.Float('Tidur Dari Jam')
    bangun_jam = fields.Float('Bangun Jam')
    total_istirahat = fields.Float('Total Istirahat')
    tanda_tangan = fields.Char('Tanda Tangan')
