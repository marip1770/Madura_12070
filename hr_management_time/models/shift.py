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


class tbl_msi_shift(models.Model):
    _name = 'tbl_msi_shift'
    _description = "Nama Shift"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

   
    name = fields.Char('Name')
    reguler = fields.Boolean('Reguler')
    duty_on = fields.Float('On Duty (days)')
    duty_off = fields.Float('Off Duty (days)')
    detail = fields.One2many('tbl_msi_shift_detail', 'details', 'Detail')
    detail_hari = fields.One2many('tbl_msi_shift_detail_hari', 'details', 'Detail Hari')


class tbl_msi_shift_detail(models.Model):
    _name = 'tbl_msi_shift_detail'
    _description = "Nama Shift_detail"

    details = fields.Many2one('tbl_msi_shift', 'Detail')  
    name = fields.Many2one('tbl_msi_jam_kerja', 'Name')
    siklus = fields.Selection([
        ('1', 'Hari Kerja 1'),
        ('2', 'Hari Kerja 2'),
        ('3', 'Hari Kerja 3'),
        ('4', 'Hari Kerja 4'),
        ('5', 'Hari Kerja 5'),
        ('6', 'Hari Kerja 6'),
        ('7', 'Hari Kerja 7'),
        ], string='Siklus', copy=False)

 

class tbl_msi_shift_detail_hari(models.Model):
    _name = 'tbl_msi_shift_detail_hari'
    _description = "Nama Shift_detail_hari"

    details = fields.Many2one('tbl_msi_shift', 'Detail')  
    name = fields.Selection([
        ('0', 'Senin'),
        ('1', 'Selasa'),
        ('2', 'Rabu'),
        ('3', 'Kamis'),
        ('4', 'Jumat'),
        ('5', 'Sabtu'),
        ('6', 'Minggu'),
        ], string='Hari', copy=False)
    jam_kerja = fields.Many2one('tbl_msi_jam_kerja', 'Name')
    siklus = fields.Selection([
        ('1', 'Hari Kerja 1'),
        ('2', 'Hari Kerja 2'),
        ('3', 'Hari Kerja 3'),
        ('4', 'Hari Kerja 4'),
        ('5', 'Hari Kerja 5'),
        ('6', 'Hari Kerja 6'),
        ('7', 'Hari Kerja 7'),
        ], string='Siklus', copy=False)

