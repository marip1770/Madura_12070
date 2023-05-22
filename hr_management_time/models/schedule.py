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


class tbl_msi_shift_schedule(models.Model):
    _name = 'tbl_msi_shift_schedule'
    _description = "Shift Schedule"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    id_gen = fields.Char('Id Gen')
    employee = fields.Many2one('hr.employee','Employee')   
    name = fields.Char('NIK')
    dept = fields.Many2one('hr.department', 'Department')
    divisi = fields.Many2one('tbl_employee_divisi', 'Divisi')
    loc = fields.Many2one('tbl_employee_lokasi', 'Lokasi')
    periode = fields.Many2one('tbl_msi_periode_bulan','Period')
    tgl001 = fields.Char('1', readonly=True)
    tgl002 = fields.Char('2', readonly=True)
    tgl003 = fields.Char('3', readonly=True)
    tgl004 = fields.Char('4', readonly=True)
    tgl005 = fields.Char('5', readonly=True)
    tgl006 = fields.Char('6', readonly=True)
    tgl007 = fields.Char('7', readonly=True)
    tgl008 = fields.Char('8', readonly=True)
    tgl009 = fields.Char('9', readonly=True)
    tgl010 = fields.Char('10', readonly=True)
    tgl011 = fields.Char('11', readonly=True)
    tgl012 = fields.Char('12', readonly=True)
    tgl013 = fields.Char('13', readonly=True)
    tgl014 = fields.Char('14', readonly=True)
    tgl015 = fields.Char('15', readonly=True)
    tgl016 = fields.Char('16', readonly=True)
    tgl017 = fields.Char('17', readonly=True)
    tgl018 = fields.Char('18', readonly=True)
    tgl019 = fields.Char('19', readonly=True)
    tgl020 = fields.Char('20', readonly=True)
    tgl021 = fields.Char('21', readonly=True)
    tgl022 = fields.Char('22', readonly=True)
    tgl023 = fields.Char('23', readonly=True)
    tgl024 = fields.Char('24', readonly=True)
    tgl025 = fields.Char('25', readonly=True)
    tgl026 = fields.Char('26', readonly=True)
    tgl027 = fields.Char('27', readonly=True)
    tgl028 = fields.Char('28', readonly=True)
    tgl029 = fields.Char('29', readonly=True)
    tgl030 = fields.Char('30', readonly=True)
    tgl031 = fields.Char('31', readonly=True)

