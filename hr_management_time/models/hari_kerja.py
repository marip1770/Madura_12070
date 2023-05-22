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


class tbl_msi_hari_kerja(models.Model):
    _name = 'tbl_msi_hari_kerja'
    _description = "Hari Kerja"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

   
    name = fields.Char('Name')
    reguler = fields.Boolean('Reguler', default=True)
    shift = fields.Many2one('tbl_msi_shift','Shift')
    jam_kerja = fields.Many2one('tbl_msi_jam_kerja','Jam Kerja')
    period_month = fields.Many2one('tbl_msi_periode_bulan','Period Month')
    detail_reguler = fields.One2many('tbl_msi_reguler','detail_regulers','Detail Reguler')
    detail_non_reguler = fields.One2many('tbl_msi_non_reguler','detail_non_regulers','Detail Non Reguler')

    @api.onchange('shift','period_month','jam_kerja')
    def _compute_nama_lengkap(self):
        self.name = str(self.shift.name).upper() + '-' + str(self.jam_kerja.name).upper() + '-' + str(self.period_month.name).upper()



class tbl_msi_reguler(models.Model):
    _name = 'tbl_msi_reguler'
    _description = "Reguler"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    detail_regulers = fields.Many2one('tbl_msi_hari_kerja','Detail Reguler')   
    day = fields.Selection([
         ('mon','Senin'),
         ('tue','Selasa'),
         ('wed','Rabu'),
         ('thu','Kamis'),
         ('fri','Jumat'),
         ('sat','Sabtu'),
         ('sun','Minggu'),
    ], string='Day', default='mon')
    jam_in = fields.Float('Sign In (hh:mm)')
    jam_out = fields.Float('Sign Out (hh:mm)')


class tbl_msi_non_reguler(models.Model):
    _name = 'tbl_msi_non_reguler'
    _description = "Non Reguler"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    detail_non_regulers = fields.Many2one('tbl_msi_hari_kerja','Detail Reguler')   
    day = fields.Selection([
         ('mon','Senin'),
         ('tue','Selasa'),
         ('wed','Rabu'),
         ('thu','Kamis'),
         ('fri','Jumat'),
         ('sat','Sabtu'),
         ('sun','Minggu'),
    ], string='Day', default='mon')
    date = fields.Date('Date')
    jam_in = fields.Float('Sign In (hh:mm)')
    jam_out = fields.Float('Sign Out (hh:mm)')



