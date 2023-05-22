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


class msi_department(models.Model):
    _inherit = "hr.department"
   
    kode = fields.Char('Kode', help='Kode untuk penghitungan lembur, PAB atau ELEKTRIFIKASI', track_visibility='onchange')
    kode_department = fields.Char('Kode Department')
