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


class tbl_msi_employee_group(models.Model):
    _name = 'tbl_msi_employee_group'
    _description = "Group Pegawai Shift"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

   
    name = fields.Char('Name')
    detail = fields.One2many('tbl_msi_employee_group_detail','details','Detail Employee')


class tbl_msi_employee_group_detail(models.Model):
    _name = 'tbl_msi_employee_group_detail'
    _description = "Group Pegawai Shift Detail"
    _order = 'employee'

    details = fields.Many2one('tbl_msi_employee_group','Detail Employee')   
    employee = fields.Many2one('hr.employee','Employee')
    name = fields.Char('NIK', related='employee.nik', store=True)
    dept = fields.Many2one('hr.department', 'Department', related='employee.department_id', store=True)
    divisi = fields.Many2one('tbl_employee_divisi', 'Divisi', related='employee.divisi', store=True)
    loc = fields.Many2one('tbl_employee_lokasi', 'Lokasi', related='employee.lokasi', store=True)
    job = fields.Char('Job Title', related='employee.job_title', store=True)
