# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class msi_users(models.Model):
    _inherit = 'res.users'


    employee_id = fields.Many2one('hr.employee','Employee', required=True) 
    akses_id = fields.One2many('tbl_payroll_akses','akses_ids', 'akses') 

 
class tbl_payroll_akses(models.Model):
    _name = 'tbl_payroll_akses'
    _description = "tbl_payroll_akses"
    _order = 'name'

    name = fields.Selection([
        ('Direksi', 'Direksi'),
        ('GM', 'GM'),
        ('MGR', 'Manager'),
        ('STAFF', 'Staff'),
        ], string='Akses', default='STAFF')
    akses_ids = fields.Many2one('res.users','Detail')