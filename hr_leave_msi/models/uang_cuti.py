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


class tbl_msi_uang_cuti(models.Model):
    _name = 'tbl_msi_uang_cuti'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

   
    name = fields.Char('Nomor', default='New', readonly=True)
    date = fields.Date('Date', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    periode_tahun = fields.Many2one('tbl_msi_periode_tahun','Period', required=True)
    alokasi_cuti = fields.Float('Alokasi Cuti')
    employee = fields.Many2one('hr.employee','Employee')
    nik = fields.Char('NIK')
    dept = fields.Char('Dept')
    divisi = fields.Char('Div')
    loc = fields.Char('Loc')
    job = fields.Char('Job')
    cuti_tersedia = fields.Float('Cuti Tersedia')
    nominal = fields.Float('Value')
    state = fields.Selection([
         ('draft','Draft'),
         ('submit','Submit'),
         ('done','Approved'),
         ('cancel','Canceled')
    ], string='State', default='draft', track_visibility='onchange')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('uang_cuti') or _('New')#

        result = super(tbl_msi_uang_cuti, self).create(vals)
        return result


class tbl_msi_uang_sisa_cuti(models.Model):
    _name = 'tbl_msi_uang_sisa_cuti'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

   
    name = fields.Char('Nomor', default='New', readonly=True)
    date = fields.Date('Date', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    periode_tahun = fields.Many2one('tbl_msi_periode_tahun','Period', required=True)
    alokasi_cuti = fields.Float('Alokasi Cuti')
    employee = fields.Many2one('hr.employee','Employee')
    nik = fields.Char('NIK')
    dept = fields.Char('Dept')
    divisi = fields.Char('Div')
    loc = fields.Char('Loc')
    job = fields.Char('Job')
    cuti_tersedia = fields.Float('Cuti Tersedia')
    cuti_diuangkan = fields.Float('Cuti Diuangkan')
    cuti_sisa = fields.Float('Cuti Sisa')
    nominal = fields.Float('Value')
    state = fields.Selection([
         ('draft','Draft'),
         ('submit','Submit'),
         ('done','Approved'),
         ('cancel','Canceled')
    ], string='State', default='draft', track_visibility='onchange')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('uang_sisa_cuti') or _('New')#

        result = super(tbl_msi_uang_sisa_cuti, self).create(vals)
        return result







