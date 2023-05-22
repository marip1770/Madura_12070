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


class tbl_msi_hari_libur(models.Model):
    _name = 'tbl_msi_hari_libur'
    _description = "Holiday"
    _order = 'date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

   
    name = fields.Char('Nama', required=True)
    date = fields.Date('Date', required=True)
    periode_tahun = fields.Many2one('tbl_msi_periode_tahun','Period', required=True)
    status = fields.Selection([
        ('LIBUR', 'LIBUR'),
        ('CUTI_BERSAMA', 'CUTI BERSAMA'),
        ], string='Status', default='LIBUR')
    ket = fields.Char('Ket')

