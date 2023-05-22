
import tempfile
import binascii
import xlrd
import logging
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo import api, fields, models
from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare

import datetime

from odoo.exceptions import Warning
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)

try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    from io import StringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')

class TblRegisterKonsolidasi(models.Model):
    _name = 'tbl_bisa_hauling_registrasi_konsolidasi'

    def _get_default_user_id_id(self):
        return self.env['res.users'].browse(self.env.uid)


    tanggal_awal = fields.Date('Tanggal Awal',required=True)
    tanggal_akhir = fields.Date('Tanggal Akhir',required=True)
    details = fields.One2many('tbl_bisa_hauling_konsolidasi_sistem', 'details', 'Detail')
    user_id = fields.Many2one('res.users','User') 
    user_id_id = fields.Many2one('res.users','User', default=lambda self: self.env.user) 
    lokasi_id = fields.Many2one('tbl_employee_lokasi','Site') 
    project_id= fields.Many2one('project.project','Project') 
    kontrak= fields.Many2one('tbl_bisa_hauling_kontrak','Kontrak') 
    details1 = fields.One2many('tbl_bisa_hauling_konsolidasi_pembanding', 'details', 'Detail')
    details2 = fields.One2many('tbl_bisa_hauling_konsolidasi', 'details', 'Detail')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Validate'),
    ], 'Status', default='draft', readonly=True)
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type')
    upload = fields.Binary('Upload')


    @api.multi
    def action_get(self):

        detail_obj = self.env['tbl_bisa_hauling_konsolidasi_sistem']
        if self.details:
            self.details.unlink()
        rec = self.env['tbl_bisa_hauling_assigment_opr_line'].search([('tanggal', '>=', self.tanggal_awal),('tanggal', '<=', self.tanggal_akhir),('lokasi', '=', self.lokasi_id.id),('nama_projek', '=', self.project_id.id),('no_kontrak', '=', self.kontrak.id),('tipe', '=', self.tipe)])
        if rec:
            for opr in rec:
                data_detail = detail_obj.create({
                        'details': self.id,
                        'tanggal': opr.tanggal,
                        'no_register': opr.no_register,
                        'berat': opr.qty_aktual,
                        'tipe': opr.tipe,
                        'nama_projek': opr.task_id.nama_projek.id,
                        'produk': opr.task_id.produk.id,
                        'unit_id': opr.task_id.unit_id.id,
                })

    @api.multi
    def create_konsolidasi_pembanding(self, values):
        # rec = self.env['bisa_fleet.vehicle'].search([('name', '=', values.get('unit_id'))],order='id desc',limit=1)
        # rec = self.env['bisa_fleet.vehicle'].search([('license_plate', '=', values.get('unit_id'))],order='id desc',limit=1)
        # if rec:
          self.env['tbl_bisa_hauling_konsolidasi_pembanding'].create({
            'details': self.id,
            'tanggal': values.get('tanggal'),
            'no_register': values.get('no_register'),
            'berat': values.get('berat'),
            'license_plate': values.get('unit_id')
          })
        # else:
        #     raise UserError(_('Unit  %s tidak di temukan' % (values.get('unit_id'), )))

    @api.multi
    def import_date(self, tanggal):
        return datetime.strptime(tanggal, DEFAULT_SERVER_DATE_FORMAT)

    @api.multi
    def action_import(self):
        if self.details1:
            self.details1.unlink()
        if self.upload:
            keys = ['tanggal', 'no_register', 'berat', 'unit_id']
            data = base64.b64decode(self.upload)
            file_input = StringIO(data.decode("utf-8"))
            file_input.seek(0)
            reader_info = []
            reader = csv.reader(file_input, delimiter=',')
            try:
                reader_info.extend(reader)
            except Exception:
                raise Warning(_("Not a valid file!"))
            values = {}
            for i in range(len(reader_info)):
                field = map(str, reader_info[i])
                values = dict(zip(keys, field))
                if values:
                    if i == 0:
                        continue
                    else:
                        # values.update({'option': self.import_option})
                        res = self.create_konsolidasi_pembanding(values)


    @api.multi
    def action_consol(self):

        detail_obj = self.env['tbl_bisa_hauling_konsolidasi']
        if self.details2:
            self.details2.unlink()
        if self.details:
            for sis in self.details:
                data_detail = detail_obj.create({
                        'details': self.id,
                        'tanggal': sis.tanggal,
                        'no_register': sis.no_register,
                        'berat': sis.berat,
                        'tipe': sis.tipe,
                        'nama_projek': sis.nama_projek.id,
                        'produk': sis.produk.id,
                        'unit_id': sis.unit_id.id,
                })
        if self.details1:
            for consol in self.details1:
                rec = self.env['tbl_bisa_hauling_konsolidasi'].search([('details', '=', self.id),('tanggal', '=', consol.tanggal),('no_register', '=', consol.no_register),('unit_id', '=', consol.unit_id.id),('tipe', '=', self.tipe)],limit=1)
                if rec:
                    rec.berat_aktual = consol.berat
                    if rec.berat_aktual == rec.berat:
                        rec.berat_konsolidasi = rec.berat
                else:
                    data_detail = detail_obj.create({
                        'details': self.id,
                        'tanggal': consol.tanggal,
                        'no_register': consol.no_register,
                        'berat_aktual': consol.berat,
                        'tipe': consol.tipe,
                        'nama_projek': consol.nama_projek.id,
                        'produk': consol.produk.id,
                        'unit_id': consol.unit_id.id,
                    })
    
    def action_validate(self):
        if self.details2:
            for rec in self.details2:
                if rec.berat_konsolidasi == 0:
                    raise UserError(_('Berat Konsolidasi tidak boleh 0'))
        self.state = 'confirm'

class TblKonsolidasiSistem(models.Model):
    _name = 'tbl_bisa_hauling_konsolidasi_sistem'
    _order = 'tanggal, lokasi_id'

    details = fields.Many2one('tbl_bisa_hauling_registrasi_konsolidasi', 'Regiter Konsolidasi')
    tanggal = fields.Date('Tanggal', readonly=True)
    no_register = fields.Char('No Register', readonly=True)
    berat = fields.Float('Berat', readonly=True)
    berat_aktual = fields.Float('Berat Aktual')
    # selisih = fields.Float('Selisih',compute='_compute_selisih')
    selisih = fields.Float('Selisih')
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type')
    nama_projek = fields.Many2one('project.project', 'Nama Project', related='details.project_id')
    produk = fields.Many2one('product.product', 'Produk')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
    ], 'Status', related='details.state')
    driver = fields.Many2one('hr.employee','Driver')
    unit_id = fields.Many2one('bisa_fleet.vehicle','Unit ID')
    lokasi_id = fields.Many2one('tbl_employee_lokasi','Site', related='details.lokasi_id') 
    project_id= fields.Many2one('project.project','Project', related='details.project_id') 
    kontrak= fields.Many2one('tbl_bisa_hauling_kontrak','Kontrak', related='details.kontrak') 


class TblKonsolidasiPembanding(models.Model):
    _name = 'tbl_bisa_hauling_konsolidasi_pembanding'

    details = fields.Many2one('tbl_bisa_hauling_registrasi_konsolidasi', 'Regiter Konsolidasi')
    tanggal = fields.Date('Tanggal', readonly=True)
    no_register = fields.Char('No Register', readonly=True)
    berat = fields.Float('Berat', readonly=True)
    berat_aktual = fields.Float('Berat Aktual')
    selisih = fields.Float('Selisih')
    unit_id = fields.Many2one('bisa_fleet.vehicle','Unit ID',compute='_compute_license_plate')
    # selisih = fields.Float('Selisih',compute='_compute_selisih')
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type', related='details.tipe')
    nama_projek = fields.Many2one('project.project', 'No Project', related='details.project_id')
    produk = fields.Many2one('product.product', 'Produk')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
    ], 'Status', related='details.state')
    driver = fields.Many2one('hr.employee','Driver')
    lokasi_id = fields.Many2one('tbl_employee_lokasi','Site', related='details.lokasi_id') 
    project_id= fields.Many2one('project.project','Project', related='details.project_id') 
    kontrak= fields.Many2one('tbl_bisa_hauling_kontrak','Kontrak', related='details.kontrak') 
    license_plate = fields.Char('No Register', readonly=True)



    @api.one
    @api.depends('license_plate')
    def _compute_license_plate(self):
        rec = self.env['bisa_fleet.vehicle'].search([('license_plate', '=', self.license_plate)],order='id desc',limit=1)
        if rec:
            self.unit_id = rec.id
    # @api.one
    # @api.depends('berat','berat_aktual')
    # def _compute_selisih(self):
    #     self.selisih = self.berat - self.berat_aktual


class TblKonsolidasi(models.Model):
    _name = 'tbl_bisa_hauling_konsolidasi'

    details = fields.Many2one('tbl_bisa_hauling_registrasi_konsolidasi', 'Regiter Konsolidasi')
    tanggal = fields.Date('Tanggal', readonly=True)
    no_register = fields.Char('No Register', readonly=True)
    berat = fields.Float('Berat', readonly=True)
    berat_aktual = fields.Float('Berat Pembanding')
    berat_konsolidasi = fields.Float('Berat Konsolidasi')
    selisih = fields.Float('Selisih',compute='_compute_selisih')
    # selisih = fields.Float('Selisih',compute='_compute_selisih')
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type')
    nama_projek = fields.Many2one('project.project', 'Nama Project', related='details.project_id')
    produk = fields.Many2one('product.product', 'Produk')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
    ], 'Status', related='details.state')
    driver = fields.Many2one('hr.employee','Driver')
    unit_id = fields.Many2one('bisa_fleet.vehicle','Unit ID')
    lokasi_id = fields.Many2one('tbl_employee_lokasi','Site', related='details.lokasi_id',store=True) 
    project_id= fields.Many2one('project.project','Project', related='details.project_id',store=True) 
    kontrak= fields.Many2one('tbl_bisa_hauling_kontrak','Kontrak', related='details.kontrak',store=True) 

    @api.one
    @api.depends('berat','berat_aktual')
    def _compute_selisih(self):
        self.selisih = self.berat - self.berat_aktual