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


class tbl_msi_leave_group(models.Model):
    _name = 'tbl_msi_leave_group'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

   
    name = fields.Char('Name')
    alokasi = fields.Float('Alokasi Hari', default=12)
    detail = fields.One2many('tbl_msi_leave_group_detail','details','Detail Employee')

    @api.one
    def action_get(self):
        line_obj = self.env['tbl_msi_leave_group_detail']
        cari = self.env['hr.employee'].search([('active', '=', True)])
        if cari:
              for hasil in cari:
                 if not hasil.is_exit:
                    header_payroll = line_obj.create({
                          'details': self.id,
                          'employee': hasil.id,
                    })


class tbl_msi_leave_group_detail(models.Model):
    _name = 'tbl_msi_leave_group_detail'
    _order = 'employee'

    details = fields.Many2one('tbl_msi_leave_group','Detail Employee')   
    employee = fields.Many2one('hr.employee','Employee')
    nik = fields.Char('NIK', related='employee.nik', store=True)
    dept = fields.Many2one('hr.department', 'Department', related='employee.department_id', store=True)
    divisi = fields.Many2one('tbl_employee_divisi', 'Divisi', related='employee.divisi', store=True)
    loc = fields.Many2one('tbl_employee_lokasi', 'Lokasi', related='employee.lokasi', store=True)
    job = fields.Char('Job Title', related='employee.job_title', store=True)
