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

import datetime

# class tbl_ops_hauling(models.Model):
#     _name = 'tbl_ops_hauling'
#     _order = 'name desc'

   
#     tanggal = fields.Date('Tanggal', track_visibility='onchange', default=fields.Date.today())
#     user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user, readonly=True)
#     name = fields.Many2one('hr.employee','Employee', track_visibility='onchange')

class TblHaulingKontrak(models.Model):
    _name = 'tbl_bisa_hauling_kontrak'
    _rec_name = 'nomor'
    _order = 'id desc'
    
    nomor = fields.Char('Nomor Kontrak')
    vendor = fields.Many2one('res.partner', 'Nama Customer')
    tgl_awal = fields.Date('Tanggal Awal Kontrak', required=True)
    tgl_akhir = fields.Date('Tanggal Akhir Kontrak', required=True)
    nama_projek = fields.Many2one('project.project', 'Nama Project')
    produk = fields.Many2one('product.product', 'Produk')
    lokasi = fields.Many2one('tbl_employee_lokasi', 'Site', required=True)
    quantity = fields.Float('Jumlah')
    uom = fields.Many2one('uom.uom', 'Satuan')
    harga = fields.Float('Harga Satuan')
    total = fields.Float('Harga Total')
    nilai_kontrak = fields.Float('Nilai Kontrak')
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
    ], 'Status', default='draft')
    qty_day = fields.Float('Jumlah Per Hari', compute='_get_qty_per_day', store=True)

    def action_create_plan(self):
        hauling_plan_obj = self.env['tbl_bisa_hauling_plan']

        start = self.tgl_awal
        end = self.tgl_akhir
        date = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]
        for i in date:
                data_hauling_plan = hauling_plan_obj.create({
                    'tanggal': i,
                    'vendor': self.vendor.id,
                    'no_kontrak': self.id,
                    'lokasi': self.lokasi.id,
                    'nama_projek': self.nama_projek.id,
                    'produk': self.produk.id,
                    'quantity': self.qty_day,
                    'uom': self.uom.id,
                    'tipe': self.tipe,
                })
        self.state = 'confirm'

    @api.depends('quantity', 'tgl_awal', 'tgl_akhir')
    def _get_qty_per_day(self):
        for rec in self:
            start = rec.tgl_awal
            end = rec.tgl_akhir
            rec.qty_day = rec.quantity / ((end-start).days+1)

class TblPlan(models.Model):
    _name = 'tbl_bisa_hauling_plan'
    _rec_name = 'tanggal'
    _order = 'tanggal'

    tanggal = fields.Date('Tanggal')
    vendor = fields.Many2one('res.partner', 'Nama Customer')
    no_kontrak = fields.Many2one('tbl_bisa_hauling_kontrak','Nomor Kontrak')
    lokasi = fields.Many2one('tbl_employee_lokasi', 'Site')
    nama_projek = fields.Many2one('project.project', 'Nama Project')
    produk = fields.Many2one('product.product', 'Produk')
    quantity = fields.Float('Jumlah Per Hari')
    uom = fields.Many2one('uom.uom', 'Satuan')
    total = fields.Float('Harga Total')
    nilai = fields.Float('Nilai Kontrak')
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
    ], 'Status', default='draft')
    detail_assigment_line = fields.One2many('tbl_bisa_detail_assigment', 'detail_assigment', 'Detail Assigment Line')
    # plan_p5m = fields.Many2one('tbl_bisa_hauling_p5m', 'Plan P5M')
    # plan_kesiapan_bekerja = fields.Many2one('tbl_bisa_hauling_p2h', 'Plan Kesiapan Bekerja')
    # plan_p2h = fields.Many2one('tbl_bisa_hauling_inspeksi_harian', 'Plan P2H')


    def get_schedule_um(self):
        detail_obj = self.env['tbl_bisa_detail_assigment']
        employee = self.env['tbl_msi_rekap_attendance'].search([('sc_date_a', '=', self.tanggal)])
        if employee:
            #unit_r = self.env['bisa_fleet.vehicle'].search([('driver_id', '=', emp.employee.address_home_id.id)])
            # raise UserError(_('Data %s telah ada di assigment' % (unit_r, )))
            for emp in employee: 
                unit_r = self.env['bisa_fleet.vehicle'].search([('driver_id', '=', emp.employee.address_home_id.id)])
                data_detail = detail_obj.create({
                        'driver': emp.employee.id,
                        'unit_id': unit_r.id,
                        'detail_assigment': self.id,
                    })


    def action_create_assigment(self):
        assigment_obj = self.env['tbl_bisa_hauling_assigment']
        p5m_obj = self.env['tbl_bisa_hauling_assigment_p5m_line']
        kesiapan_obj = self.env['tbl_bisa_hauling_assigment_kesiapan_line']
        p2h_obj = self.env['tbl_bisa_hauling_assigment_p2h_line']
        
        cari_driver = assigment_obj
        if self.detail_assigment_line:
            for dc in self.detail_assigment_line:
                rec = cari_driver.search([('driver','=',dc.driver.id),('tanggal','=',self.tanggal),('tipe','=',self.tipe)], limit=1)
                if rec:
                    raise UserError(_('Data %s telah ada di assigment' % (dc.driver.name, )))
                else:
                    data_assigment = assigment_obj.create({
                        'tanggal': self.tanggal, 
                        'nama_projek': self.nama_projek.id, 
                        'no_kontrak': self.no_kontrak.id, 
                        'produk': self.produk.id,
                        'qty_rencana': self.quantity,
                        'uom': self.uom.id,
                        'lokasi':self.lokasi.id,
                        'route':dc.route.id,
                        'lokasi_asal': dc.lokasi_asal,
                        'lokasi_tujuan': dc.lokasi_tujuan,
                        'driver': dc.driver.id,
                        'unit_id': dc.unit_id.id,
                        'route': dc.route.id,
                        'lokasi': dc.lokasi.id,
                        'tipe': self.tipe,
                    })

                    rec_p5m = self.env['tbl_bisa_hauling_p5m'].search([('tipe','=',self.tipe)], limit=1, order="id desc")
                    for p5m_tmpl in rec_p5m.data_p5m_line:
                        data_p5m_assigment = p5m_obj.create({
                            'field_pertanyaan_p5m': p5m_tmpl.pertanyaan_p5m,
                            'normal_value': p5m_tmpl.normal_value,
                            'assigment_line_p5m': data_assigment.id,
                        })

                    rec_kesiapan = self.env['tbl_bisa_hauling_kesiapan_bekerja'].search([('tipe','=',self.tipe)], limit=1, order="id desc")
                    for kesiapan_tmpl in rec_kesiapan.data_kesiapan_line:
                        data_kesiapan_assigment = kesiapan_obj.create({
                            'field_pertanyaan_kesiapan': kesiapan_tmpl.pertanyaan_kesiapan,
                            'normal_value': kesiapan_tmpl.normal_value,
                            'assigment_line_kesiapan': data_assigment.id,
                        })

                    rec_p2h = self.env['tbl_bisa_hauling_p2h'].search([('tipe','=',self.tipe),('tipe_unit','=',dc.unit_id.tipe)], limit=1, order="id desc")
                    for p2h_tmpl in rec_p2h.data_p2h_line:
                        data_p2h_assigment = p2h_obj.create({
                            'field_pertanyaan_p2h': p2h_tmpl.pertanyaan_p2h,
                            'normal_value': p2h_tmpl.normal_value,
                            'assigment_line_p2h': data_assigment.id,
                        })
                self.state = 'confirm'

class TblDetailAssigment(models.Model):
    _name = 'tbl_bisa_detail_assigment'

    driver = fields.Many2one('hr.employee','Nama Driver')
    unit_id = fields.Many2one('bisa_fleet.vehicle','Unit ID')
    tipe_driver = fields.Selection([
        ('truck', 'Truck'),
        ('alat', 'Alat'),
    ], 'Tipe Driver', related='driver.tipe_driver')
    no_kontrak = fields.Many2one('tbl_bisa_hauling_kontrak','Nomor Kontrak', related='detail_assigment.no_kontrak')
    # lokasi_asal = fields.Many2one('tbl_employee_lokasi','Lokasi Asal')
    route = fields.Many2one('tbl_bisa_route','Route')
    lokasi = fields.Many2one('tbl_employee_lokasi', 'Site', related='detail_assigment.lokasi')
    lokasi_asal = fields.Selection([
        ('PORT', 'PORT'),
        ('PIT', 'PIT'),
        ('ROM', 'ROM'),
    ],'Lokasi Asal', compute='_get_lokasi_asal_tujuan', store=True)
    lokasi_tujuan = fields.Selection([
        ('PORT', 'PORT'),
        ('PIT', 'PIT'),
        ('ROM', 'ROM'),
    ],'Lokasi Tujuan', compute='_get_lokasi_asal_tujuan', store=True)
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type')
    detail_assigment = fields.Many2one('tbl_bisa_hauling_plan', 'Detail Assigment')

    @api.one
    @api.depends('lokasi_asal', 'lokasi_tujuan', 'route.asal', 'route.tujuan')
    def _get_lokasi_asal_tujuan(self):
        if self.route.asal:
            self.lokasi_asal = self.route.asal
        if self.route.tujuan:
            self.lokasi_tujuan = self.route.tujuan


class TblAssigment(models.Model):
    _name = 'tbl_bisa_hauling_assigment'
    _rec_name = 'name'
    _order = 'tanggal'
    
    tanggal = fields.Date('Tanggal')
    no_kontrak = fields.Many2one('tbl_bisa_hauling_kontrak','Nomor Kontrak')
    name = fields.Char('Nomor Assigment', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    qty_aktual = fields.Float('Jumlah Aktual', compute='_get_berat_timbangan', store=True)
    driver = fields.Many2one('hr.employee','Nama Driver')
    unit_id = fields.Many2one('bisa_fleet.vehicle','Unit ID')
    user_driver = fields.Many2one('res.users', 'User Driver', compute='_get_user_driver', store=True)
    state = fields.Selection([
        ('start','Start'),
        ('p5m','P5M'),
        ('kesiapan','Kesiapan'),
        ('p2h','P2H'),
        ('operasional','Operasional'),
        ('done','Done'),
        ('maintenance', 'Maintenance'),
        ('cancel','Cancel'),
    ], 'Assigment Status', default='start')
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type')
    # lokasi_asal = fields.Many2one('tbl_employee_lokasi','Lokasi Asal')
    # lokasi_tujuan = fields.Many2one('tbl_employee_lokasi','Lokasi Tujuan')
    lokasi = fields.Many2one('tbl_employee_lokasi', 'Site')
    lokasi_asal = fields.Selection([
        ('PORT', 'PORT'),
        ('PIT', 'PIT'),
        ('ROM', 'ROM'),
    ],'Lokasi Asal')
    lokasi_tujuan = fields.Selection([
        ('PORT', 'PORT'),
        ('PIT', 'PIT'),
        ('ROM', 'ROM'),
    ],'Lokasi Tujuan')
    route = fields.Many2one('tbl_bisa_route','Route')
    nama_projek = fields.Many2one('project.project', 'Nama Project')
    produk = fields.Many2one('product.product', 'Produk')
    qty_rencana = fields.Float('Jumlah Rencana Per Hari')
    uom = fields.Many2one('uom.uom', 'Satuan')
    field_jumlah_nilai = fields.Float('Jumlah Nilai', compute='_get_hitung_jumlah', store=True)
    operasional_line = fields.One2many('tbl_bisa_hauling_assigment_opr_line', 'task_id', 'Operasional Line')
    p5m_line = fields.One2many('tbl_bisa_hauling_assigment_p5m_line', 'assigment_line_p5m', 'P5M Line')
    kesiapan_line = fields.One2many('tbl_bisa_hauling_assigment_kesiapan_line', 'assigment_line_kesiapan', 'Kesiapan Line')
    p2h_line = fields.One2many('tbl_bisa_hauling_assigment_p2h_line', 'assigment_line_p2h', 'P2H Line')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if vals.get('tipe', _('hauling')) == ('hauling'):
                vals['name'] = self.env['ir.sequence'].next_by_code('seq_no_register_hauling') or _('New')
            if vals.get('tipe', _('hrm')) == ('hrm'):
                vals['name'] = self.env['ir.sequence'].next_by_code('seq_no_register_hrm') or _('New')
            if vals.get('tipe', _('rental')) == ('rental'):
                vals['name'] = self.env['ir.sequence'].next_by_code('seq_no_register_rental') or _('New')
            if vals.get('tipe', _('port')) == ('port'):
                vals['name'] = self.env['ir.sequence'].next_by_code('seq_no_register_port') or _('New')
            if vals.get('tipe', _('fuel_truck')) == ('fuel_truck'):
                vals['name'] = self.env['ir.sequence'].next_by_code('seq_no_register_fuel_truck') or _('New')
            if vals.get('tipe', _('water_truck')) == ('water_truck'):
                vals['name'] = self.env['ir.sequence'].next_by_code('seq_no_register_water_truck') or _('New')
            if vals.get('tipe', _('tls')) == ('tls'):
                vals['name'] = self.env['ir.sequence'].next_by_code('seq_no_register_tls') or _('New')
        result = super(TblAssigment, self).create(vals)
        return result
    
    @api.one
    @api.depends('driver')
    def _get_user_driver(self):
        if self.driver:
            self.user_driver = self.driver.user_id.id

    @api.depends('qty_aktual', 'operasional_line', 'operasional_line.qty_aktual')
    def _get_berat_timbangan(self):
        for jumlah_timbangan in self:
            qty_aktual = 0.0
            for ops_line in jumlah_timbangan.operasional_line:
                qty_aktual += ops_line.qty_aktual
            jumlah_timbangan.update({
                'qty_aktual': qty_aktual,
            })

    @api.depends('field_jumlah_nilai','p2h_line','p2h_line.field_nilai')
    def _get_hitung_jumlah(self):
        for jumlah in self:
            field_jumlah_nilai = 0.0
            for line in jumlah.p2h_line:
                field_jumlah_nilai += line.field_nilai
            jumlah.update({
                'field_jumlah_nilai': field_jumlah_nilai,
            })

    def action_p5m(self):
        for rec in self:
            rec.state = 'p5m'

    @api.multi
    def action_kesiapan(self):
        if self.p5m_line:
            for check_p5m in self.p5m_line:
                rec_p5m = self.env['tbl_bisa_hauling_assigment_p5m_line'].search([('id', '=', check_p5m.id),('normal_value','!=', check_p5m.field_jawaban_p5m)])
                if rec_p5m:
                    self.state = 'cancel'
                acc_p5m = self.env['tbl_bisa_hauling_assigment_p5m_line'].search([('id', '=', check_p5m.id),('normal_value','=', check_p5m.field_jawaban_p5m)], limit=1)
                if acc_p5m:
                    self.state = 'kesiapan'

    def action_p2h(self):
        for rec in self:
            rec.state = 'p2h'

    @api.multi
    def action_operasional(self):
        if self.p2h_line:
            if self.field_jumlah_nilai == 0:
                self.state = 'operasional'
            if self.field_jumlah_nilai > 0:
                maintenance_obj = self.env['tbl_bisa_work_request_dept']
                data_maintenance = maintenance_obj.create({
                        'request_user': self.driver.id,
                        'departement': self.driver.department_id.id,
                        'task_id': self.id,
                })
                detail_maintenance_obj = self.env['tbl_bisa_detail_wrd']
                for dc in self.p2h_line:
                    if dc.field_nilai == 1:
                        data_detail_maintenance = detail_maintenance_obj.create({
                            'description': dc.field_pertanyaan_p2h,
                            'remark': dc.field_jawaban_p2h,
                            'data': data_maintenance.id,
                        })
                self.state = 'maintenance'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

class TblAssigmentOprLine(models.Model):
    _name = 'tbl_bisa_hauling_assigment_opr_line'

    tanggal = fields.Date('Tanggal', compute='_get_name_line_opr', store=True)
    # task_id = fields.Char('Task ID')
    start_time = fields.Char('Start Time')
    geo_start_longtitude = fields.Char('Start Long')
    geo_start_latitude = fields.Char('Start Lat')
    end_time = fields.Char('End Time')
    geo_end_longtitude = fields.Char('End Long')
    geo_end_latitude = fields.Char('End Lat')  
    start_shift = fields.Char('Start Shift')
    geo_shift_start_longtitude = fields.Char('Shift Start Long')
    geo_shift_start_latitude = fields.Char('Shift Start Lat') 
    end_shift = fields.Char('End Shift')
    geo_shift_end_longtitude = fields.Char('Shift End Long')
    geo_shift_end_latitude = fields.Char('Shift End Lat')
    no_register = fields.Char('Nomor Register')
    qty_aktual = fields.Float('Jumlah Aktual')
    uom = fields.Many2one('uom.uom', 'Satuan')
    start_pengisian = fields.Char('Start Pengisian')
    geo_pengisian_start_longtitude = fields.Char('Pengisian Start Long')
    geo_pengisian_start_latitude = fields.Char('Pengisian Start Lat')
    end_pengisian = fields.Char('End Pengisian')
    geo_pengisian_end_longtitude = fields.Char('Pengisian End Long')
    geo_pengisian_end_latitude = fields.Char('Pengisian End Lat')
    id_unit = fields.Many2one('bisa_fleet.vehicle','ID Unit', compute='_get_name_line_opr', store=True)
    user_driver = fields.Many2one('res.users', 'User Driver', compute='_get_name_line_opr', store=True)
    driver = fields.Many2one('hr.employee','Nama Driver', compute='_get_name_line_opr', store=True)
    # c = fields.Char('')
    # d = fields.Char('')
    fuel_meter_start = fields.Char('Fuel Meter Start')
    fuel_meter_end = fields.Char('Fuel Meter End')
    hm_km = fields.Char('HM/KM')
    start_hm = fields.Char('Start HM')
    end_hm = fields.Char('End HM')
    kondisi = fields.Char('Kondisi')
    picture = fields.Binary('Upload Gambar')
    no_lambung = fields.Char('Nomor Lambung')
    deskripsi = fields.Char('Deskripsi')
    nama_projek = fields.Many2one('project.project', 'Nama Project', related='task_id.nama_projek')
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type', compute='_get_name_line_opr', store=True)
    route = fields.Many2one('tbl_bisa_route','Route', related='task_id.route', store=True)
    task_id = fields.Many2one('tbl_bisa_hauling_assigment','Operasional')
    lokasi = fields.Many2one('tbl_employee_lokasi', 'Site', related='task_id.lokasi', store=True)
    no_kontrak = fields.Many2one('tbl_bisa_hauling_kontrak','Nomor Kontrak', related='task_id.no_kontrak', store=True)
    
    @api.one
    @api.depends('tanggal','user_driver','driver','id_unit','task_id','no_register','uom','tipe')
    def _get_name_line_opr(self):
        if self.task_id:
            self.tanggal = self.task_id.tanggal
            self.user_driver = self.task_id.user_driver.id
            self.id_unit = self.task_id.unit_id.id
            self.driver = self.task_id.driver.id
            # self.no_register = self.task_id.name
            self.uom = self.task_id.uom.id
            self.tipe = self.task_id.tipe

class TblAssigmentP5mLine(models.Model):
    _name = 'tbl_bisa_hauling_assigment_p5m_line'

    user_driver = fields.Many2one('res.users', 'User Driver', compute='_get_name_line_p5m', store=True)
    field_pertanyaan_p5m = fields.Char('Pertanyaan')
    field_jawaban_p5m = fields.Selection([
        ('Ya', 'Ya'),
        ('Tidak', 'Tidak'),
    ],'Jawaban')
    normal_value = fields.Selection([
        ('Ya', 'Ya'),
        ('Tidak', 'Tidak'),
    ],'Normal Value')
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type', compute='_get_name_line_p5m')
    assigment_line_p5m = fields.Many2one('tbl_bisa_hauling_assigment','P5M')

    @api.one
    @api.depends('assigment_line_p5m','user_driver','tipe')
    def _get_name_line_p5m(self):
        if self.assigment_line_p5m:
            self.user_driver = self.assigment_line_p5m.user_driver.id
            self.tipe = self.assigment_line_p5m.tipe

class TblAssigmentKesiapanLine(models.Model):
    _name = 'tbl_bisa_hauling_assigment_kesiapan_line'

    user_driver = fields.Many2one('res.users', 'User Driver', compute='_get_name_line_kesiapan', store=True)
    field_pertanyaan_kesiapan = fields.Char('Pertanyaan')
    field_jawaban_kesiapan = fields.Float('Jawaban')
    normal_value = fields.Char('Normal Value')
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type', compute='_get_name_line_kesiapan')
    assigment_line_kesiapan = fields.Many2one('tbl_bisa_hauling_assigment','Kesiapan')

    @api.one
    @api.depends('assigment_line_kesiapan','user_driver','tipe')
    def _get_name_line_kesiapan(self):
        if self.assigment_line_kesiapan:
            self.user_driver = self.assigment_line_kesiapan.user_driver.id
            self.tipe = self.assigment_line_kesiapan.tipe

class TblAssigmentP2hLine(models.Model):
    _name = 'tbl_bisa_hauling_assigment_p2h_line'

    unit_id = fields.Many2one('bisa_fleet.vehicle','Unit ID', compute='_get_name_line_p2h', store=True)
    field_pertanyaan_p2h = fields.Char('Pertanyaan')
    field_jawaban_p2h = fields.Selection([
        ('Baik', 'Baik'),
        ('Kurang', 'Kurang'),
        ('Rusak', 'Rusak'),
    ], 'Jawaban')
    normal_value = fields.Selection([
        ('Baik', 'Baik'),
        ('Kurang', 'Kurang'),
        ('Rusak', 'Rusak'),
    ], 'Normal Value')
    field_nilai = fields.Float('Nilai', compute='_get_biner', store=True)
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type', compute='_get_name_line_p2h')
    assigment_line_p2h = fields.Many2one('tbl_bisa_hauling_assigment','P2H')

    @api.one
    @api.depends('assigment_line_p2h','unit_id','tipe')
    def _get_name_line_p2h(self):
        if self.assigment_line_p2h:
            self.unit_id = self.assigment_line_p2h.unit_id.id
            self.tipe = self.assigment_line_p2h.tipe

    @api.depends('assigment_line_p2h','field_nilai')
    def _get_biner(self):
        for check_p2h in self:
            rec_p2h = self.env['tbl_bisa_hauling_assigment_p2h_line'].search([('id', '=', check_p2h.id),('normal_value', '!=', check_p2h.field_jawaban_p2h)])
            if rec_p2h:
                check_p2h.field_nilai = '1'
            else:
                check_p2h.field_nilai = '0'

class TblHaulingP5m(models.Model):
    _name = 'tbl_bisa_hauling_p5m'
    _rec_name = 'nomor'

    nomor = fields.Char('Nomor Dokumen', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    tgl_terbit = fields.Date('Tanggal Terbit Dokumen', default=fields.Date.today())
    revisi = fields.Integer('Revisi')
    # tanggal = fields.Date('Tanggal')
    departemen = fields.Many2one('hr.department','Departemen')
    nama_projek = fields.Many2one('project.project', 'Nama Project')
    lokasi = fields.Many2one('tbl_employee_lokasi','Site')
    pemateri = fields.Char('Pemberi Materi')
    # jml_peserta = fields.Integer('Jumlah Peserta')
    data_p5m_line = fields.One2many('tbl_bisa_hauling_data_p5m', 'p5m_line', 'Data P5M Line')
    # absensi_line = fields.One2many('tbl_bisa_hauling_absensi_p5m', 'absensi', 'Absensi Line')
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type', required=True)

    @api.model
    def create(self, vals):
        if vals.get('nomor', _('New')) == _('New'):
            if vals.get('tipe', _('hauling')) == ('hauling'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p5m_hauling') or _('New')
            if vals.get('tipe', _('hrm')) == ('hrm'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p5m_hrm') or _('New')
            if vals.get('tipe', _('rental')) == ('rental'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p5m_rental') or _('New')
            if vals.get('tipe', _('port')) == ('port'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p5m_port') or _('New')
            if vals.get('tipe', _('fuel_truck')) == ('fuel_truck'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p5m_fuel_truck') or _('New')
            if vals.get('tipe', _('water_truck')) == ('water_truck'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p5m_water_truck') or _('New')
            if vals.get('tipe', _('tls')) == ('tls'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p5m_tls') or _('New')
        result = super(TblHaulingP5m, self).create(vals)
        return result

    # @api.model
    # def create(self, vals):
    #     if vals.get('nomor', _('New')) == _('New'):
    #             vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p5m') or _('New')
    #     result = super(TblHaulingP5m, self).create(vals)
    #     return result

class TblHaulingDataP5m(models.Model):
    _name = 'tbl_bisa_hauling_data_p5m'

    pertanyaan_p5m = fields.Char('Pertanyaan')
    normal_value = fields.Selection([
        ('Ya', 'Ya'),
        ('Tidak', 'Tidak'),
    ],'Normal Value')
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type', compute='_get_tipe', store=True)
    p5m_line = fields.Many2one('tbl_bisa_hauling_p5m', 'P5M Line')

    @api.one
    @api.depends('p5m_line','tipe')
    def _get_tipe(self):
        if self.p5m_line:
            self.tipe = self.p5m_line.tipe

# class TblHaulingAbsensi(models.Model):
#     _name = 'tbl_bisa_hauling_absensi_p5m'

#     sn = fields.Integer('SN')
#     nama = fields.Char('Nama')
#     departemen = fields.Many2one('hr.department','Departemen')
#     # tanda_tangan = fields.Char('Tanda Tangan')
#     tipe = fields.Selection([
        # ('hauling', 'Hauling'),
        # ('hrm', 'HRM'),
        # ('rental', 'Rental'),
        # ('port', 'Port'),
        # ('fuel_truck', 'Fuel Truck'),
        # ('water_truck', 'Water Truck'),
        # ('tls', 'TLS'),
#     ], 'Type')
#     absensi = fields.Many2one('tbl_bisa_hauling_p5m', 'Absensi')

class TblEmployeeP5m(models.Model):
    _inherit = 'hr.employee'

    # template_p5m = fields.One2many('tbl_bisa_hauling_data_template_p5m', 'employee','P5M')
    # template_kesiapan = fields.One2many('tbl_bisa_hauling_data_template_kesiapan', 'employee', 'Kesiapan Bekerja')
    tipe_driver = fields.Selection([
        ('truck', 'Truck'),
        ('alat', 'Alat'),
    ], 'Tipe Driver')    
    # lokasi = fields.Many2one('tbl_employee_lokasi','Lokasi')

# class TblTemplate(models.Model):
#     _name = 'tbl_bisa_hauling_data_template_p5m'
#     _rec_name = 'data_template_p5m'

#     data_template_p5m = fields.Many2one('tbl_bisa_hauling_p5m', 'Template P5M')
#     employee = fields.Many2one('hr.employee', 'Employee')

# class TblTemplate(models.Model):
#     _name = 'tbl_bisa_hauling_data_template_kesiapan'
#     _rec_name = 'data_template_kesiapan'

#     data_template_kesiapan = fields.Many2one('tbl_bisa_hauling_kesiapan_bekerja', 'Template Kesiapan')
#     employee = fields.Many2one('hr.employee', 'Employee')

class TblHaulingKesiapanBekerja(models.Model):
    _name = 'tbl_bisa_hauling_kesiapan_bekerja'
    _rec_name = 'nomor'

    nomor = fields.Char('Nomor Dokumen', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    tgl_terbit = fields.Date('Tanggal Terbit Dokumen', default=fields.Date.today())
    revisi = fields.Integer('Revisi')
    nama_projek = fields.Many2one('project.project', 'Nama Project')
    lokasi = fields.Many2one('tbl_employee_lokasi','Site')
    data_kesiapan_line = fields.One2many('tbl_bisa_hauling_data_kesiapan_bekerja', 'kesiapan_line', 'Data Kesiapan Line')
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type', required=True)

    @api.model
    def create(self, vals):
        if vals.get('nomor', _('New')) == _('New'):
            if vals.get('tipe', _('hauling')) == ('hauling'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_kesiapan_hauling') or _('New')
            if vals.get('tipe', _('hrm')) == ('hrm'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_kesiapan_hrm') or _('New')
            if vals.get('tipe', _('rental')) == ('rental'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_kesiapan_rental') or _('New')
            if vals.get('tipe', _('port')) == ('port'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_kesiapan_port') or _('New')
            if vals.get('tipe', _('fuel_truck')) == ('fuel_truck'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_kesiapan_fuel_truck') or _('New')
            if vals.get('tipe', _('water_truck')) == ('water_truck'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_kesiapan_water_truck') or _('New')
            if vals.get('tipe', _('tls')) == ('tls'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_kesiapan_tls') or _('New')
        result = super(TblHaulingKesiapanBekerja, self).create(vals)
        return result

    # @api.model
    # def create(self, vals):
    #     if vals.get('nomor', _('New')) == _('New'):
    #             vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_kesiapan') or _('New')
    #     result = super(TblHaulingKesiapanBekerja, self).create(vals)
    #     return result

class TbHaulinglDataKesiapanBekerja(models.Model):
    _name = 'tbl_bisa_hauling_data_kesiapan_bekerja'

    pertanyaan_kesiapan = fields.Char('Pertanyaan')
    normal_value = fields.Char('Normal Value')
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type', compute='_get_tipe', store=True)
    kesiapan_line = fields.Many2one('tbl_bisa_hauling_kesiapan_bekerja', 'Kesiapan Line')

    @api.one
    @api.depends('kesiapan_line','tipe')
    def _get_tipe(self):
        if self.kesiapan_line:
            self.tipe = self.kesiapan_line.tipe

class TblHaulingP2h(models.Model):
    _name = 'tbl_bisa_hauling_p2h'
    _rec_name = 'nomor'

    nomor = fields.Char('Nomor Dokumen', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    tgl_terbit = fields.Date('Tanggal Terbit Dokumen', default=fields.Date.today())
    revisi = fields.Integer('Revisi')
    nama_projek = fields.Many2one('project.project', 'Nama Project')
    lokasi = fields.Many2one('tbl_employee_lokasi','Site')
    data_p2h_line = fields.One2many('tbl_bisa_hauling_data_p2h', 'p2h_line', 'Data P2H Line')
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type', required=True)
    tipe_unit = fields.Selection([
        ('truck', 'Truck'),
        ('alat', 'Alat'),
    ], 'Type Unit', required=True)

    @api.model
    def create(self, vals):
        if vals.get('nomor', _('New')) == _('New'):
            if vals.get('tipe', _('hauling')) == ('hauling'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p2h_hauling') or _('New')
            if vals.get('tipe', _('hrm')) == ('hrm'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p2h_hrm') or _('New')
            if vals.get('tipe', _('rental')) == ('rental'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p2h_rental') or _('New')
            if vals.get('tipe', _('port')) == ('port'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p2h_port') or _('New')
            if vals.get('tipe', _('fuel_truck')) == ('fuel_truck'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p2h_fuel_truck') or _('New')
            if vals.get('tipe', _('water_truck')) == ('water_truck'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p2h_water_truck') or _('New')
            if vals.get('tipe', _('tls')) == ('tls'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p2h_tls') or _('New')
        result = super(TblHaulingP2h, self).create(vals)
        return result

    # @api.model
    # def create(self, vals):
    #     if vals.get('nomor', _('New')) == _('New'):
    #             vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_p2h') or _('New')
    #     result = super(TblHaulingP2h, self).create(vals)
    #     return result

class TblHaulingDataP2h(models.Model):
    _name = 'tbl_bisa_hauling_data_p2h'

    pertanyaan_p2h = fields.Char('Pertanyaan')
    normal_value = fields.Selection([
    ('Baik', 'Baik'),
    ('Kurang', 'Kurang'),
    ('Rusak', 'Rusak'),
    ], 'Normal Value')
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type', compute='_get_tipe', store=True)
    p2h_line = fields.Many2one('tbl_bisa_hauling_p2h', 'P2H Line')

    @api.one
    @api.depends('p2h_line','tipe')
    def _get_tipe(self):
        if self.p2h_line:
            self.tipe = self.p2h_line.tipe

class TblRoute(models.Model):
    _name = 'tbl_bisa_route'

    name = fields.Char('Deskripsi', compute='_get_name', store=True)
    lokasi = fields.Many2one('tbl_employee_lokasi', 'Site', required=True)
    nomor_lokasi_asal = fields.Char('Nomor Lokasi Asal')
    asal = fields.Selection([
        ('PORT', 'PORT'),
        ('PIT', 'PIT'),
        ('ROM', 'ROM'),
    ], 'Asal',required=True)
    nomor_lokasi_tujuan = fields.Char('Nomor Lokasi Tujuan')
    tujuan = fields.Selection([
        ('PORT', 'PORT'),
        ('PIT', 'PIT'),
        ('ROM', 'ROM'),
    ],'Tujuan',required=True)
    jarak = fields.Float('Jarak(KM)',required=True)

    @api.one
    @api.depends('nomor_lokasi_asal','asal','nomor_lokasi_tujuan','tujuan')
    def _get_name(self):
        if self.asal or self.tujuan:
            self.name = str(self.asal)+str(self.nomor_lokasi_asal)+" - "+str(self.tujuan)+str(self.nomor_lokasi_tujuan)

# class TblProduksi(models.Model):
#     _name = 'tbl_bisa_ops_produksi'

#     no = fields.Char('NO')
#     type_unit = fields.Char('Type Unit')
#     tipe = fields.Char('Type')
#     code_number = fields.Char('Code Number')
#     production = fields.Char('Production')
#     general = fields.Char('General')
#     total_working_hrs = fields.Char('Total Working Hours')
#     bd = fields.Char('BD')
#     stby = fields.Char('STBY')
#     moh = fields.Char('MOH')
#     pa = fields.Char('PA%')
#     ua = fields.Char('UA%')
#     keterangan = fields.Char('Keterangan')


# class TblPenggunaanBBM(models.Model):
#     _name = 'tbl_bisa_bbm'

#     no = fields.Char('NO')
#     nama_alat = fields.Char('Nama Alat')
#     jam_operasi_unit_s1 = fields.Char('Jam Operasi Unit (Shift 1)')
#     jam_operasi_unit_s2 = fields.Char('Jam Operasi Unit (Shift 2)')
#     total = fields.Char('Total')
#     pengisian_bbm_s1 = fields.Char('Pengisian BBM (Shift 1)')
#     pengisian_bbm_s2 = fields.Char('Pengisian BBM (Shift 2)')
#     fr = fields.Char('F.R')


# class TblMaUnit(models.Model):
#     _name = 'tbl_bisa_ma_unit'

#     no = fields.Char('NO')
#     nama_unit = fields.Char('Nama Unit')
#     total_jam_operasional = fields.Char('Total Jam Operasional')
#     bd_schedule = fields.Char('BD Schedule (MAintenance)')
#     non_schedule = fields.Char('Non Schedule')
#     total_jam_bd = fields.Char('Total Jam BD')
#     ma = fields.Char('MA%')
#     average_ma = fields.Char('Average MA')
    