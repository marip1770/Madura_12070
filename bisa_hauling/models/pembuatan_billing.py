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

class tbl_pembuatan_billing(models.Model):
    _name = 'tbl_pembuatan_billing'
    _order = 'name desc'

    tanggal = fields.Date('Tanggal', default=fields.Date.today())
    user = fields.Many2one('res.users','User', default=lambda self: self.env.user, readonly=True)
    name = fields.Char('Nomor', default='New', readonly=True)
    nama_projek = fields.Many2one('project.project', 'Nama Project', required=True)
    lokasi = fields.Many2one('tbl_employee_lokasi', 'Site', required=True)
    produk = fields.Many2one('product.product', 'Produk')
    tgl_awal = fields.Date('Tanggal Awal', required=True)
    tgl_akhir = fields.Date('Tanggal Akhir', required=True)
    kontrak= fields.Many2one('tbl_bisa_hauling_kontrak','Kontrak') 
    details = fields.One2many('tbl_pembuatan_billing_detail', 'details', 'Detail')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
    ], 'Status', default='draft')
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type', required=True)

    @api.one
    def action_get(self):

        detail_obj = self.env['tbl_pembuatan_billing_detail']
        if self.details:
            self.details.unlink()
        total = 0
        rec = self.env['tbl_bisa_hauling_konsolidasi'].search([('tanggal', '>=', self.tgl_awal),('tanggal', '<=', self.tgl_akhir),('nama_projek', '=', self.nama_projek.id),('lokasi_id', '=', self.lokasi.id),('kontrak', '=', self.kontrak.id)])
        # kontrak = self.env['tbl_bisa_hauling_kontrak'].search([('produk', '=', self.produk.id),('nama_projek', '=', self.nama_projek.id)], limit=1)
        if rec:
            total = 0
            for opr in rec:
                total += opr.berat_konsolidasi
        data_detail = detail_obj.create({
                        'details': self.id,
                        'produk': self.produk.id,
                        'nama_projek': self.nama_projek.id,
                        'quantity': total,
                        'uom': self.kontrak.uom.id,
                        'harga': self.kontrak.harga,
                        # 'total': kontrak.harga * total,
        })

    def action_create_bill(self):

        detail_obj = self.env['account.invoice']
        detail_line_obj = self.env['account.invoice.line']
        if self.details:
            data_detail = detail_obj.create({
                        'partner_id': self.kontrak.vendor.id,
                        'date_invoice': self.tanggal,
                        'create_billing_id': self.id,
            })
            # raise UserError(_('aaaaa'))
            for data in self.details:
                data_detail_line = detail_line_obj.create({
                        'invoice_id': data_detail.id,
                        'produk': self.kontrak.produk.id,
                        'account_id': self.kontrak.produk.property_account_income_id.id,
                        'name': 'Hauling Periode '+str(self.tgl_awal)+' - '+str(self.tgl_akhir),
                        'quantity': data.quantity,
                        'uom_id': data.uom.id,
                        'harga': data.harga,
                        'rf': data.rf,
                        'distance': data.distance,
                        'price_unit': data.new_harga,
                        # 'total': kontrak.harga * total,
                })


class tbl_pembuatan_billing_detail(models.Model):
    _name = 'tbl_pembuatan_billing_detail'
    
    details = fields.Many2one('tbl_pembuatan_billing', 'Pembuatan Billing')
    produk = fields.Many2one('product.product', 'Produk')
    nama_projek = fields.Many2one('project.project', 'Nama Project', related='details.nama_projek')
    lokasi = fields.Many2one('tbl_employee_lokasi', 'Site', related='details.lokasi')
    quantity = fields.Float('Volume')
    uom = fields.Many2one('uom.uom', 'Satuan')
    harga = fields.Float('Base Rate')
    rf = fields.Float('RF')
    new_harga = fields.Float('New Rate',compute='_compute_new_harga')
    distance = fields.Float('Distance')
    total = fields.Float('Gross Amount',compute='_compute_total')
    nilai_kontrak = fields.Float('Nilai Kontrak')
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Type', related='details.tipe')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
    ], 'Status', related='details.state')

    @api.one
    @api.depends('harga','rf')
    def _compute_new_harga(self):
        self.new_harga = self.harga + self.rf

    @api.one
    @api.depends('quantity','new_harga','distance')
    def _compute_total(self):
        self.total = self.quantity * self.new_harga * self.distance