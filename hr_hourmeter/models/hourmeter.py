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



class tbl_msi_hourmeter_input(models.Model):
    _name = 'tbl_msi_hourmeter_input'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

   
    name = fields.Date('Tanggal', track_visibility='onchange', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ('done', 'Done'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    detail = fields.One2many('tbl_msi_hourmeter','details','Hourmeter Detail')

    def action_submit(self):
        self.state = 'submit'

    def action_approve(self):
        self.state = 'approve'
        if self.detail:
           for hm in self.detail:
               hm.parameter_ch = fields.Datetime.now()


    def action_done(self):
        self.state = 'done'


class tbl_msi_hourmeter(models.Model):
    _name = 'tbl_msi_hourmeter'
    _order = 'date desc'

    details = fields.Many2one('tbl_msi_hourmeter_input','Hourmeter Detail')    
    date = fields.Date('Date', related='details.name',  store=True)
    user = fields.Many2one('res.users','User', track_visibility='onchange', related='details.user')
    employee = fields.Many2one('hr.employee','Employee')
    name = fields.Char('NIK')
    mesin_id = fields.Many2one('tbl_msi_master_mesin', 'Transportasi')
    jam = fields.Float('Durasi')

    persen = fields.Float('Pencapaian Produksi (%)')
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

        for record in self: 
            if record.persen == 0:                   
               record.nominal = int(record.jam * record.mesin_id.rate)
            else:                   
               record.nominal = int(record.jam * record.mesin_id.rate * (record.persen/100))
 


 


