# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2018 Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round



class msi_print_invoice(models.Model):
    _inherit = "account.invoice"

    no_kontrak = fields.Char('Kontrak No')
    faktur_pajak = fields.Char('Faktur Pajak')

    total = fields.Char('Amount Total')
    dasar_pengenaan_pajak = fields.Char('Amount Untaxed')
    ppn = fields.Char('Amount tax')
    print_date_invoice = fields.Char('Date invoice1')
    residual1 = fields.Char('Residual1')

    no_rek = fields.Many2one('tbl_msi_rekening','Transfer Ke')


    @api.multi
    def do_print_invoice(self):
        if not self.no_rek:
            raise UserError(_('Transfer Ke Belum Di Tentukan'))
        if self.date_invoice:
            tahun = str(self.date_invoice)[0:4]
            bulan = str(self.date_invoice)[5:7]
            tanggal = str(self.date_invoice)[8:10]
            self.print_date_invoice = str(tanggal)+'/'+str(bulan)+'/'+str(tahun)
        else:
            self.print_date_invoice = '-'

        self.total = '{:,}'.format(float(self.amount_total))
        self.dasar_pengenaan_pajak = '{:,}'.format(float(self.amount_untaxed))
        self.ppn = '{:,}'.format(float(self.amount_tax))
        self.residual1 = '{:,}'.format(float(self.residual))
        return self.env.ref('msi_print_accounting.action_print_invoice').report_action(self)

    @api.multi
    def do_print_kwitansi(self):
        if self.date_invoice:
            tahun = str(self.date_invoice)[0:4]
            bulan = str(self.date_invoice)[5:7]
            tanggal = str(self.date_invoice)[8:10]
            self.print_date_invoice = str(tanggal)+'/'+str(bulan)+'/'+str(tahun)
        else:
            self.print_date_invoice = '-'

        self.total = '{:,}'.format(float(self.amount_total))

        return self.env.ref('msi_print_accounting.action_print_invoice_kwitansi').report_action(self)
    
    # @api.onchange('date_invoice')
    # def onchange_date_invoice(self):
    #     self.date_invoice:
    #         tahun = str(self.date_invoice)[0:4]
    #         bulan = str(self.date_invoice)[5:7]
    #         tanggal = str(self.date_invoice0)[8:10]
    #         self.print_date_invoice = str(tanggal)+'/'+str(bulan)+'/'+str(tahun)

class tbl_msi_rekening(models.Model):
    _name = 'tbl_msi_rekening'
    _order = 'name desc'

    name = fields.Char('Rekening', compute='_compute_rekening', store=True)
    atas_nama = fields.Char('Atas Nama', required=True)
    nama_bank = fields.Char('Nama Bank', required=True)
    no_rek = fields.Char('No Rekening', required=True)


    @api.one
    @api.depends('atas_nama','nama_bank','no_rek')
    def _compute_rekening(self):
    	if self.atas_nama and self.no_rek and self.nama_bank:
            self.name = str(self.atas_nama)+' / '+str(self.no_rek)+' ('+str(self.nama_bank)+')'

class msi_print_po_order_line (models.Model):
    _inherit = "account.invoice.line"

    price_unit1 = fields.Char('Price Unit1',compute='_compute_price_unit')
    price_subtotal1 = fields.Char('Price Subtotal',compute='_compute_price_unit')
    # hs_code = fields.Many2one('tbl_hscode_list','HS Code',related="product_id.hs_code", store=True)#,related="product_id.hs_code", store=True
    # akl = fields.Many2one('tbl_msi_akl_new','AKL',)#related="product_id.akl_id", store=True


    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     if self.product_id:
    #         self.akl = self.product_id.akl_id
    #         self.hs_code = self.product_id.hs_code

    @api.one
    @api.depends('price_unit','price_subtotal')
    def _compute_price_unit(self):
        self.price_unit1 = '{:,}'.format(float(self.price_unit))
        self.price_subtotal1 = '{:,}'.format(float(self.price_subtotal))       
        

class msi_print_payment(models.Model):
    _inherit = "account.payment"

    departemen = fields.Many2one('account.analytic.tag','Departemen')
    no_kwitansi = fields.Char('Kwitansi Number', readonly=True)
    print_payment_date = fields.Char('Print Payment Date')
    print_amount = fields.Char('Print Amount')
    print_departemen = fields.Char('Print Departemen')

    @api.multi
    def do_print_voucher_pengeluaran(self):
        tahun = str(self.payment_date)[0:4]
        bulan = str(self.payment_date)[5:7]
        tanggal = str(self.payment_date)[8:10]
        self.print_payment_date = str(tanggal)+'/'+str(bulan)+'/'+str(tahun)

        if self.departemen:
            self.print_departemen = self.departemen.name
        else:
            self.print_departemen = '-'

        self.print_amount = '{:,}'.format(float(self.amount))
        return self.env.ref('msi_print_accounting.action_print_voucher_pengeluaran').report_action(self)
    @api.multi
    def do_print_voucher_penerimaan(self):
        tahun = str(self.payment_date)[0:4]
        bulan = str(self.payment_date)[5:7]
        tanggal = str(self.payment_date)[8:10]
        self.print_payment_date = str(tanggal)+'/'+str(bulan)+'/'+str(tahun)

        if self.departemen:
            self.print_departemen = self.departemen.name
        else:
            self.print_departemen = '-'

        self.print_amount = '{:,}'.format(float(self.amount))
        return self.env.ref('msi_print_accounting.action_print_voucher_penerimaan').report_action(self)
    @api.multi
    def do_print_kwitansi(self):
        tahun = str(self.payment_date)[0:4]
        bulan = str(self.payment_date)[5:7]
        tanggal = str(self.payment_date)[8:10]
        self.print_payment_date = str(tanggal)+'/'+str(bulan)+'/'+str(tahun)

        self.print_amount = '{:,}'.format(float(self.amount))

        if not self.no_kwitansi:
            self.no_kwitansi = self.env['ir.sequence'].next_by_code('acc_kwitansi')

        return self.env.ref('msi_print_accounting.action_print_kwitansi').report_action(self)