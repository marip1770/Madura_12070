# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import calendar
from odoo import api, fields, models
from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare

class tbl_msi_hr_structure_tax(models.Model):
    _name = 'tbl_msi_hr_structure_tax'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char('Name')
    date = fields.Date('Date', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    ket = fields.Char('Keterangan')  
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

class tbl_tax_biaya_jabatan(models.Model):
    _name = 'tbl_tax_biaya_jabatan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char('Name')
    nilai_maks = fields.Float('Nilai Maksimum')
    nilai_persen = fields.Float('Persen(%)')
    ket = fields.Char('Keterangan') 


class tbl_tax_period(models.Model):
    _name = 'tbl_tax_period'
    _description = "Tax Periode"
    _order = 'date_awal'
   
    name = fields.Char('Month', required=True)
    tahun = fields.Many2one('tbl_tax_year','Tahun', required=True)
    date_awal = fields.Date('Date Start', required=True)
    date_akhir = fields.Date('Date End', required=True)
    bulan_ke = fields.Char('Bulan(angka)')
    ket = fields.Char('Ket')

class tbl_generate_tax_period(models.Model):
    _name = 'tbl_generate_tax_period'
    _description = "Generate Tax Periode"
    _order = 'name'
   
    # name = fields.Char('Month', required=True)
    name = fields.Many2one('tbl_tax_year','Tahun', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ], string='Status', readonly=True, copy=False, index=True, default='draft')
    ket = fields.Char('Ket')

    @api.one
    def action_generate(self):
        tax_period_obj = self.env['tbl_tax_period']
        cari = self.env['tbl_generate_tax_period'].search([('name', '=', self.name.id),('id', '!=', self.id)])
        if cari:
            raise UserError(_(("period %s sudah tergenerate") % (self.name.name)))
        else:
            self.state = 'done'
            bulan_awal = 1

            while bulan_awal < 13:
              tes = calendar.monthrange(self.name.value, bulan_awal)[1]
              my_string = str(self.name.name)+'-'+str(bulan_awal)+'-01' 
              my_end = str(self.name.name)+'-'+str(bulan_awal)+'-'+str(tes)

  # Create date object in given time format yyyy-mm-dd
              my_date = datetime.strptime(my_string, "%Y-%m-%d")
              my_date_end = datetime.strptime(my_end, "%Y-%m-%d")
              nama = ''
              if bulan_awal == 1:
                nama = 'JAN '+str(self.name.name)
              if bulan_awal == 2:
                nama = 'FEB '+str(self.name.name)
              if bulan_awal == 3:
                nama = 'MAR '+str(self.name.name)
              if bulan_awal == 4:
                nama = 'APR '+str(self.name.name)
              if bulan_awal == 5:
                nama = 'MEI '+str(self.name.name)
              if bulan_awal == 6:
                nama = 'JUN '+str(self.name.name)
              if bulan_awal == 7:
                nama = 'JUL '+str(self.name.name)
              if bulan_awal == 8:
                nama = 'AGU '+str(self.name.name)
              if bulan_awal == 9:
                nama = 'SEP '+str(self.name.name)
              if bulan_awal == 10:
                nama = 'OKT '+str(self.name.name)
              if bulan_awal == 11:
                nama = 'NOV '+str(self.name.name)
              if bulan_awal == 12:
                nama = 'DES '+str(self.name.name)
              # print(my_date).date()
              # print(my_date_end).date()
              data_line2 = tax_period_obj.create({
                      'name': nama,
                      'tahun': self.name.id,
                      'date_awal': my_date.date(),
                      'date_akhir': my_date_end.date(),
                      'ket': self.ket,
              }) 
              bulan_awal += 1

class tbl_tax_year(models.Model):
    _name = 'tbl_tax_year'
    _description = "Tax Year"
    _order = 'value desc'
   
    name = fields.Char('Name', required=True)
    value = fields.Integer('Tahun', required=True)

