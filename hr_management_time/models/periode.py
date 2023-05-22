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


class tbl_msi_periode_tahun(models.Model):
    _name = 'tbl_msi_periode_tahun'
    _order = 'date_awal desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
   
    name = fields.Char()
    tahun = fields.Float('Year', required=True, digits=(4,0))
    date_awal = fields.Date('Date Start', required=True)
    date_akhir = fields.Date('Date End', required=True)
    ket = fields.Char('Ket')

    @api.onchange('tahun')
    def _compute_nama_lengkap(self):
        self.name = str(self.tahun)


class tbl_msi_periode_bulan(models.Model):
    _name = 'tbl_msi_periode_bulan'
    _order = 'date_awal desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
   
    name = fields.Char('Month', required=True)
    date_awal = fields.Date('Date Start', required=True)
    date_akhir = fields.Date('Date End', required=True)
    ket = fields.Char('Ket')

