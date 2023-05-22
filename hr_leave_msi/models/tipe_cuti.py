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

class tbl_msi_cuti_tipe(models.Model):
    _name = 'tbl_msi_cuti_tipe'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char('Name')
#     alloc_date = fields.Float('Day Allocation')
    alloc_date = fields.Float('Leave Eligibitity (days)')
    tipe = fields.Selection([
         ('tanggungan','Tanggungan'),
         ('diluar_tanggungan','Diluar Tanggungan'),
    ], string='Type', default='tanggungan', track_visibility='onchange')
    is_pc = fields.Boolean('Potong Cuti')
    is_uang_cuti = fields.Boolean('Uang Cuti')
