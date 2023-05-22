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


class tbl_msi_retase_input(models.Model):
    _name = 'tbl_msi_retase_input'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

   
    name = fields.Char('Nomor', default='New', readonly=True)
    date = fields.Date('Date', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    employee = fields.Many2one('hr.employee','Employee', track_visibility='onchange')
    nik = fields.Char('NIK')
    periode = fields.Many2one('tbl_msi_periode_bulan', 'Period', track_visibility='onchange')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    detail = fields.One2many('tbl_msi_retase','details','Retase Detail')


class tbl_msi_retase(models.Model):
    _name = 'tbl_msi_retase'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    details = fields.Many2one('tbl_msi_retase_input','Retase Detail')   
    date = fields.Date('Date', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    employee = fields.Many2one('hr.employee','Employee', related='details.user')
    nik = fields.Char('NIK', related='details.nik')
    periode = fields.Many2one('tbl_msi_periode_bulan', 'Period', related='details.periode')
    trip_id = fields.Many2one('tbl_msi_master_trip', 'Trip Name')
    unit_id = fields.Many2one('tbl_msi_master_unit', 'Unit Name')
    qty = fields.Float('qty')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft', related='details.state')