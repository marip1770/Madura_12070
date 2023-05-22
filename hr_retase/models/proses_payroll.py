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


class tbl_msi_proses_payroll(models.Model):
    _name = 'tbl_msi_proses_payroll'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

   

    name = fields.Date('Tanggal', track_visibility='onchange', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    periode = fields.Many2one('tbl_msi_periode_bulan','Periode', track_visibility='onchange')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    detail = fields.One2many('tbl_msi_proses_payroll_detail','details','Proses Payroll Detail')


    def act_get_data(self):
        detail_obj = self.env['tbl_msi_proses_payroll_detail']
      
        if self.detail:
           self.detail.unlink()

        self.env.cr.execute('SELECT date, employee, name, route_id, transportasi_id, jam FROM tbl_msi_retase\
                             WHERE date >= %s and date <= %s' ,(self.periode.date_awal, self.periode.date_akhir))

        for row in self.env.cr.fetchall():

                 data_line2 = detail_obj.create({
                    'details': self.id,
                    'date': row[0],
                    'employee': row[1],
                    'name': row[2],
                    'route_id': row[3],
                    'transportasi_id': row[4],
                    'jam': row[5],
                 })

class tbl_msi_proses_payroll_detail(models.Model):
    _name = 'tbl_msi_proses_payroll_detail'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    details = fields.Many2one('tbl_msi_proses_payroll','Proses Payroll Detail')   
    date = fields.Date('Date')
    user = fields.Many2one('res.users','User', track_visibility='onchange', related='details.user' )
    employee = fields.Many2one('hr.employee','Employee')
    name = fields.Char('NIK')
    route_id = fields.Many2one('tbl_msi_master_route', 'Route')
    transportasi_id = fields.Many2one('tbl_msi_master_transport', 'Transportasi')
    jam = fields.Float('Jam')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft', related='details.state')