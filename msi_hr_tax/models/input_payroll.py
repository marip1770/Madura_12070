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



class tbl_msi_tax_input(models.Model):
    _name = 'tbl_msi_tax_input'
    _description = "tbl_msi_tax_input"
    _order = 'details desc'

    payroll_date = fields.Date('Payroll Date', required=True)
    details = fields.Char('Detail')
    name = fields.Char('Name')
    kode = fields.Char('Code')
    tipe = fields.Char('Type')
    nominal = fields.Float('Nominal')
    employee = fields.Char('Employee',)
    nik = fields.Char('NIK')
    tipe_potongan = fields.Char(string='Tipe Potongan')
    date = fields.Date('Date', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )

