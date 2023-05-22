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

class tbl_hr_sanksi(models.Model):
    _name = 'tbl_hr_sanksi'
    _order = 'name desc'

   
    tanggal = fields.Date('Tanggal', track_visibility='onchange', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user, readonly=True)

    name = fields.Many2one('hr.employee','Employee', track_visibility='onchange')
    nik = fields.Char('NIK', track_visibility='onchange')
    tipe = fields.Many2one('tbl_hr_tipe_sanksi','Tipe', track_visibility='onchange')
    desc = fields.Text('Deskripsi', track_visibility='onchange')
    tindak_lanjut = fields.Text('Tindak Lanjut', track_visibility='onchange')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    @api.onchange('name')
    def onchange_name(self):
        if self.name:
        	self.nik = self.name.nik

class tbl_hr_tipe_sanksi(models.Model):
    _name = 'tbl_hr_tipe_sanksi'
    _order = 'name desc'
    
    name = fields.Char('Tipe Sanksi', track_visibility='onchange')
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user, readonly=True)
