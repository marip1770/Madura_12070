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


class tbl_msi_jam_kerja(models.Model):
    _name = 'tbl_msi_jam_kerja'
    _description = "Jam Kerja"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

   
    name = fields.Char('Name', track_visibility='onchange')
    jam_in = fields.Float('Sign In (hh:mm)', track_visibility='onchange')
    jam_out = fields.Float('Sign Out (hh:mm)', track_visibility='onchange')
    overnight = fields.Boolean('Overnight', track_visibility='onchange')
    durasi = fields.Float('Durasi Kerja (Jam)', track_visibility='onchange')
    overtime = fields.Float('Automatic Overtime', help='Lembur Otomatis dikarenakan kelebihan jam kerja', track_visibility='onchange')
    kode = fields.Char('Kode', help='Kode untuk penghitungan lembur, N3 utk lembur N3', track_visibility='onchange')

    tol_terlambat = fields.Float('Toleransi Terlambat (Menit)', default=10, help='Nilai yg menunjukkan mulai dihitung sebagai terlambat setelah menit ke - xx', track_visibility='onchange')
    max_lama_terlambat = fields.Float('Maks Terlambat (jam)', default=1, help='Nilai yg menunjukkan mulai dikurangi lembur harian setelah terlambat xx jam', track_visibility='onchange')
    min_lama_cepat_pulang = fields.Float('Minimal Pulang Cepat (Jam)', default=1, help='Nilai yg menunjukkan mulai dikurangi lembur harian setelah pulang cepat xx jam', track_visibility='onchange')

