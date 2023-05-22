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


class tbl_msi_retase_input(models.Model):
    _name = 'tbl_msi_retase_input'
    _order = 'name desc'

   

    name = fields.Date('Tanggal', track_visibility='onchange', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ('done', 'Done'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    detail = fields.One2many('tbl_msi_retase','details','Retase Detail')

    def action_submit(self):
        self.state = 'submit'

    def action_approve(self):
        self.state = 'approve'
        if self.detail:
           for hm in self.detail:
               hm.parameter_ch = fields.Datetime.now()


    def action_done(self):
        self.state = 'done'



class tbl_msi_retase(models.Model):
    _name = 'tbl_msi_retase'
    _order = 'date desc'

    details = fields.Many2one('tbl_msi_retase_input','Retase Detail')
    date = fields.Date('Tanggal', track_visibility='onchange', related='details.name', store=True)
    user = fields.Many2one('res.users','User', track_visibility='onchange', related='details.user')
    employee = fields.Many2one('hr.employee','Employee')
    name = fields.Char('NIK')
    route_id = fields.Many2one('tbl_msi_master_route', 'Route')
    transportasi_id = fields.Many2one('tbl_msi_master_transport', 'Transportasi')
    jam = fields.Float('Durasi')
    pencapaian = fields.Float('Pencapaian (%)', help='Prosentasi Pencapaian Target')
    nominal = fields.Float('Nominal', help='Nominal dalam Rp', compute='_compute_nominal', store=True,)
    parameter_ch = fields.Char('Parameter', help='Keterangan', readonly=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ('done', 'Done'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft', related='details.state')

    @api.onchange('employee')
    def _compute_employee(self):
        if self.employee:
            self.name = self.employee.nik


    @api.depends('parameter_ch')
    def _compute_nominal(self):
        transport=0
        for record in self:
            if record.pencapaian >= 90:         
               # cari_param = self.env['tbl_msi_driver_position'].sudo().search([('name', '=', self.employee.id)], limit=1 )
               # if cari_param:
               transport = record.transportasi_id.rate
            
               record.nominal = round(record.jam * 47.24 * transport)
            else:               
               record.nominal = 0

class tbl_msi_retase_input_driver(models.Model):
    _name = 'tbl_msi_retase_input_driver'
    _order = 'name desc'

    name = fields.Date('Tanggal', track_visibility='onchange', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ('done', 'Done'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    detail = fields.One2many('tbl_msi_retase_driver','details','Retase Driver Detail')

    def action_submit(self):
        self.state = 'submit'

    def action_approve(self):
        self.state = 'approve'
        if self.detail:
           for hm in self.detail:
               hm.parameter_ch = fields.Datetime.now()


    def action_done(self):
        self.state = 'done'



class tbl_msi_retase_driver(models.Model):
    _name = 'tbl_msi_retase_driver'
    _order = 'date desc'

    details = fields.Many2one('tbl_msi_retase_input_driver','Retase Driver Detail')
    date = fields.Date('Tanggal', track_visibility='onchange', related='details.name', store=True)
    user = fields.Many2one('res.users','User', track_visibility='onchange', related='details.user')
    driver = fields.Many2one('tbl_msi_driver_position','Driver', required=True)
    id_employee = fields.Integer('ID Nama Driver', related='driver.id_employee', store=True)
    name = fields.Char('NIK', related='driver.nik')
    route_id = fields.Many2one('tbl_msi_master_route', 'Route')
    # transportasi_id = fields.Many2one('tbl_msi_master_transport', 'Transportasi')
    jam = fields.Float('Durasi')
    pencapaian = fields.Float('Pencapaian (%)', help='Prosentasi Pencapaian Target')
    nominal = fields.Float('Nominal', help='Nominal dalam Rp', compute='_compute_nominal', store=True,)
    parameter_ch = fields.Char('Parameter', help='Keterangan', readonly=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ('done', 'Done'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft', related='details.state')


    @api.depends('parameter_ch')
    def _compute_nominal(self):
        driver=0
        for record in self:
            if record.jam:         
               driver = record.driver.rate
               record.nominal = record.jam * driver



