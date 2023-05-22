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


class tbl_msi_master_uang_cuti(models.Model):
    _name = 'tbl_msi_master_uang_cuti'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

   
    name = fields.Many2one('tbl_msi_cuti_tipe', 'Name')
    nominal = fields.Selection([
         ('gapok','Gaji Pokok'),
         ('manual','Manual'),
    ], string='Nominal', default='gapok', track_visibility='onchange')

    is_cuti_pertama = fields.Boolean('Cuti Pertama')
    is_cuti_minimal = fields.Boolean('Minumun Durasi')
    durasi = fields.Float('Durasi Cuti')
