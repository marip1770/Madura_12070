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

# class tbl_ops_contract_management(models.Model):
#     _name = 'tbl_ops_contract_management'
#     _order = 'name desc'

   
#     tanggal = fields.Date('Tanggal', track_visibility='onchange', default=fields.Date.today())
#     user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user, readonly=True)
#     name = fields.Many2one('hr.employee','Employee', track_visibility='onchange')

class TblContractManagement(models.Model):
    _name = 'tbl_bisa_contract_management'
    _rec_name = 'no_kontrak'
    _order = 'id desc'

    name = fields.Many2one('sale.order', 'Nomor Sales Order')
    no_kontrak = fields.Char('Nomor Kontrak', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    tanggal = fields.Date('Tanggal Pembuatan Kontrak', default=fields.Date.today())
    nama_customer = fields.Many2one('res.partner', 'Nama Customer')
    tgl_kontrak_awal = fields.Date('Tanggal Awal Kontrak')
    tgl_kontrak_akhir = fields.Date('Tanggal Akhir Kontrak')
    # jaminan = fields.Char('Jaminan')
    # tgl_jaminan_awal = fields.Date('Tanggal Awal')
    # tgl_jaminan_akhir = fields.Date('Tanggal Akhir')
    nilai = fields.Float('Total Nilai Kontrak', compute='_amount_all', store=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('done','Done'),
    ], 'Status', default='draft')
    detail_contrak = fields.One2many('tbl_bisa_detail_contract', 'detailcontrak', 'Detail Kontrak')
    detail_progress = fields.One2many('tbl_bisa_progress', 'detailprogress', 'Detail Progress')

    @api.model
    def create(self, vals):
        if vals.get('no_kontrak', _('New')) == _('New'):
            vals['no_kontrak'] = self.env['ir.sequence'].next_by_code('seq_kontrak') or _('New')
        result = super(TblContractManagement, self).create(vals)
        return result

    def action_create(self):
        hauling_obj = self.env['tbl_bisa_hauling_kontrak']
        
        # cari_hauling = self.env['tbl_bisa_detail_contract'].search([('detailcontrak','=',self.id)], limit=1)
        if self.detail_contrak:
            for dc in self.detail_contrak:
                if not dc.nama_projek:
                    raise UserError(_('Nama Projek pada %s belum di isi' % (dc.produk.name, )))
                if dc.is_confirm == False:
                    if dc.produk.servis == 'hauling':
                        data_kontrak = hauling_obj.create({
                            'nomor': self.no_kontrak,
                            'vendor': self.nama_customer.id,
                            'tgl_awal': self.tgl_kontrak_awal,
                            'tgl_akhir': self.tgl_kontrak_akhir,
                            'nilai_kontrak': self.nilai,
                            'nama_projek': dc.nama_projek.id,
                            'produk': dc.produk.id,
                            'lokasi': dc.lokasi.id,
                            'quantity': dc.quantity,
                            'uom': dc.uom.id,
                            'harga': dc.harga,
                            'total': dc.total,
                            'tipe': 'hauling',
                        })
                        dc.is_confirm = True
                
                    if dc.produk.servis == 'hrm':
                        data_kontrak = hauling_obj.create({
                            'nomor': self.no_kontrak,
                            'vendor': self.nama_customer.id,
                            'tgl_awal': self.tgl_kontrak_awal,
                            'tgl_akhir': self.tgl_kontrak_akhir,
                            'nilai_kontrak': self.nilai,
                            'nama_projek': dc.nama_projek.id,
                            'produk': dc.produk.id,
                            'lokasi': dc.lokasi.id,
                            'quantity': dc.quantity,
                            'uom': dc.uom.id,
                            'harga': dc.harga,
                            'total': dc.total,
                            'tipe': 'hrm',
                        })
                        dc.is_confirm = True
                    
                    if dc.produk.servis == 'rental':
                        data_kontrak = hauling_obj.create({
                            'nomor': self.no_kontrak,
                            'vendor': self.nama_customer.id,
                            'tgl_awal': self.tgl_kontrak_awal,
                            'tgl_akhir': self.tgl_kontrak_akhir,
                            'nilai_kontrak': self.nilai,
                            'nama_projek': dc.nama_projek.id,
                            'produk': dc.produk.id,
                            'lokasi': dc.lokasi.id,
                            'quantity': dc.quantity,
                            'uom': dc.uom.id,
                            'harga': dc.harga,
                            'total': dc.total,
                            'tipe': 'rental',
                        })
                        dc.is_confirm = True

                    if dc.produk.servis == 'port':
                        data_kontrak = hauling_obj.create({
                            'nomor': self.no_kontrak,
                            'vendor': self.nama_customer.id,
                            'tgl_awal': self.tgl_kontrak_awal,
                            'tgl_akhir': self.tgl_kontrak_akhir,
                            'nilai_kontrak': self.nilai,
                            'nama_projek': dc.nama_projek.id,
                            'produk': dc.produk.id,
                            'lokasi': dc.lokasi.id,
                            'quantity': dc.quantity,
                            'uom': dc.uom.id,
                            'harga': dc.harga,
                            'total': dc.total,
                            'tipe': 'port',
                        })
                        dc.is_confirm = True

                    if dc.produk.servis == 'fuel_truck':
                        data_kontrak = hauling_obj.create({
                            'nomor': self.no_kontrak,
                            'vendor': self.nama_customer.id,
                            'tgl_awal': self.tgl_kontrak_awal,
                            'tgl_akhir': self.tgl_kontrak_akhir,
                            'nilai_kontrak': self.nilai,
                            'nama_projek': dc.nama_projek.id,
                            'produk': dc.produk.id,
                            'lokasi': dc.lokasi.id,
                            'quantity': dc.quantity,
                            'uom': dc.uom.id,
                            'harga': dc.harga,
                            'total': dc.total,
                            'tipe': 'fuel_truck',
                        })
                        dc.is_confirm = True

                    if dc.produk.servis == 'water_truck':
                        data_kontrak = hauling_obj.create({
                            'nomor': self.no_kontrak,
                            'vendor': self.nama_customer.id,
                            'tgl_awal': self.tgl_kontrak_awal,
                            'tgl_akhir': self.tgl_kontrak_akhir,
                            'nilai_kontrak': self.nilai,
                            'nama_projek': dc.nama_projek.id,
                            'produk': dc.produk.id,
                            'lokasi': dc.lokasi.id,
                            'quantity': dc.quantity,
                            'uom': dc.uom.id,
                            'harga': dc.harga,
                            'total': dc.total,
                            'tipe': 'water_truck',
                        })
                        dc.is_confirm = True

                    if dc.produk.servis == 'tls':
                        data_kontrak = hauling_obj.create({
                            'nomor': self.no_kontrak,
                            'vendor': self.nama_customer.id,
                            'tgl_awal': self.tgl_kontrak_awal,
                            'tgl_akhir': self.tgl_kontrak_akhir,
                            'nilai_kontrak': self.nilai,
                            'nama_projek': dc.nama_projek.id,
                            'produk': dc.produk.id,
                            'lokasi': dc.lokasi.id,
                            'quantity': dc.quantity,
                            'uom': dc.uom.id,
                            'harga': dc.harga,
                            'total': dc.total,
                            'tipe': 'tls',
                        })
                        dc.is_confirm = True
                self.state = 'done'

    @api.depends('nilai','detail_contrak','detail_contrak.total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            nilai = 0.0
            for line in order.detail_contrak:
                nilai += line.total
            order.update({
                'nilai': nilai,
            })

class TblDetailKontrak(models.Model):
    _name = 'tbl_bisa_detail_contract'

    nama_projek = fields.Many2one('project.project', 'Nama Project', required=True)
    produk = fields.Many2one('product.product', 'Produk')
    nama_customer = fields.Many2one('res.partner', 'Nama Customer',related='detailcontrak.nama_customer')
    # lokasi = fields.Char('Lokasi')
    lokasi = fields.Many2one('tbl_employee_lokasi', 'Site', required=True)
    quantity = fields.Float('QTY')
    uom = fields.Many2one('uom.uom', 'Satuan')
    harga = fields.Float('Harga Satuan')
    total = fields.Float('Harga Total', compute='_get_total', store=True)
    progress = fields.Char('Progress')
    invoiced = fields.Char('Invoiced')
    bayar = fields.Char('Paid')
    is_confirm = fields.Boolean('Is Confirm')
    detailcontrak = fields.Many2one('tbl_bisa_contract_management', 'Kontrak')

    @api.depends('quantity','harga')
    def _get_total(self):
        for rec in self:
            rec.total = rec.quantity * rec.harga
    
    def action_create_line(self):
        hauling_obj = self.env['tbl_bisa_hauling_kontrak']
        
        if self.is_confirm == False:
            if self.produk.servis == 'hauling':
                    data_kontrak = hauling_obj.create({
                        'nomor': self.detailcontrak.no_kontrak,
                        'vendor': self.detailcontrak.nama_customer.id,
                        'tgl_awal': self.detailcontrak.tgl_kontrak_awal,
                        'tgl_akhir': self.detailcontrak.tgl_kontrak_akhir,
                        'nilai_kontrak': self.detailcontrak.nilai,
                        'nama_projek': self.nama_projek.id,
                        'produk': self.produk.id,
                        'lokasi': self.lokasi.id,
                        'quantity': self.quantity,
                        'harga': self.harga,
                        'total': self.total,
                        'tipe': 'hauling',
                    })
                    self.is_confirm = True

            if self.produk.servis == 'hrm':
                    data_kontrak = hauling_obj.create({
                        'nomor': self.detailcontrak.no_kontrak,
                        'vendor': self.detailcontrak.nama_customer.id,
                        'tgl_awal': self.detailcontrak.tgl_kontrak_awal,
                        'tgl_akhir': self.detailcontrak.tgl_kontrak_akhir,
                        'nilai_kontrak': self.detailcontrak.nilai,
                        'nama_projek': self.nama_projek.id,
                        'produk': self.produk.id,
                        'lokasi': self.lokasi.id,
                        'quantity': self.quantity,
                        'harga': self.harga,
                        'total': self.total,
                        'tipe': 'hrm',
                    })
                    self.is_confirm = True

            if self.produk.servis == 'rental':
                    data_kontrak = hauling_obj.create({
                        'nomor': self.detailcontrak.no_kontrak,
                        'vendor': self.detailcontrak.nama_customer.id,
                        'tgl_awal': self.detailcontrak.tgl_kontrak_awal,
                        'tgl_akhir': self.detailcontrak.tgl_kontrak_akhir,
                        'nilai_kontrak': self.detailcontrak.nilai,
                        'nama_projek': self.nama_projek.id,
                        'produk': self.produk.id,
                        'lokasi': self.lokasi.id,
                        'quantity': self.quantity,
                        'harga': self.harga,
                        'total': self.total,
                        'tipe': 'rental',
                    })
                    self.is_confirm = True

            if self.produk.servis == 'port':
                    data_kontrak = hauling_obj.create({
                        'nomor': self.detailcontrak.no_kontrak,
                        'vendor': self.detailcontrak.nama_customer.id,
                        'tgl_awal': self.detailcontrak.tgl_kontrak_awal,
                        'tgl_akhir': self.detailcontrak.tgl_kontrak_akhir,
                        'nilai_kontrak': self.detailcontrak.nilai,
                        'nama_projek': self.nama_projek.id,
                        'produk': self.produk.id,
                        'lokasi': self.lokasi.id,
                        'quantity': self.quantity,
                        'harga': self.harga,
                        'total': self.total,
                        'tipe': 'port',
                    })
                    self.is_confirm = True

            if self.produk.servis == 'fuel_truck':
                    data_kontrak = hauling_obj.create({
                        'nomor': self.detailcontrak.no_kontrak,
                        'vendor': self.detailcontrak.nama_customer.id,
                        'tgl_awal': self.detailcontrak.tgl_kontrak_awal,
                        'tgl_akhir': self.detailcontrak.tgl_kontrak_akhir,
                        'nilai_kontrak': self.detailcontrak.nilai,
                        'nama_projek': self.nama_projek.id,
                        'produk': self.produk.id,
                        'lokasi': self.lokasi.id,
                        'quantity': self.quantity,
                        'harga': self.harga,
                        'total': self.total,
                        'tipe': 'fuel_truck',
                    })
                    self.is_confirm = True

            if self.produk.servis == 'water_truck':
                    data_kontrak = hauling_obj.create({
                        'nomor': self.detailcontrak.no_kontrak,
                        'vendor': self.detailcontrak.nama_customer.id,
                        'tgl_awal': self.detailcontrak.tgl_kontrak_awal,
                        'tgl_akhir': self.detailcontrak.tgl_kontrak_akhir,
                        'nilai_kontrak': self.detailcontrak.nilai,
                        'nama_projek': self.nama_projek.id,
                        'produk': self.produk.id,
                        'lokasi': self.lokasi.id,
                        'quantity': self.quantity,
                        'harga': self.harga,
                        'total': self.total,
                        'tipe': 'water_truck',
                    })
                    self.is_confirm = True

            if self.produk.servis == 'tls':
                    data_kontrak = hauling_obj.create({
                        'nomor': self.detailcontrak.no_kontrak,
                        'vendor': self.detailcontrak.nama_customer.id,
                        'tgl_awal': self.detailcontrak.tgl_kontrak_awal,
                        'tgl_akhir': self.detailcontrak.tgl_kontrak_akhir,
                        'nilai_kontrak': self.detailcontrak.nilai,
                        'nama_projek': self.nama_projek.id,
                        'produk': self.produk.id,
                        'lokasi': self.lokasi.id,
                        'quantity': self.quantity,
                        'harga': self.harga,
                        'total': self.total,
                        'tipe': 'tls',
                    })
                    self.is_confirm = True
            

class TblProgress(models.Model):
    _name = 'tbl_bisa_progress'

    no_invoice = fields.Char('Nomor Invoice')
    produk = fields.Char('Produk')
    progress = fields.Char('Progress')
    nominal = fields.Char('Nominal')
    detailprogress = fields.Many2one('tbl_bisa_contract_management', 'Progress')

class TblInheritProduct(models.Model):
    _inherit = 'product.product'

    servis = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Service')

# class TblLokasi(models.Model):
#     _name = 'tbl_bisa_kontrak_lokasi'

#     name = fields.Char('Nama Lokasi')

# class TblProjek(models.Model):
#     _inherit = 'project.project'

#     name = fields.Char('No Project', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    
#     @api.model
#     def create(self, vals):
#         if vals.get('name', _('New')) == _('New'):
#             vals['name'] = self.env['ir.sequence'].next_by_code('seq_projek') or _('New')
#         result = super(TblProjek, self).create(vals)
#         return result