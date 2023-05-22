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

import datetime

# class tbl_ops_plan(models.Model):
#     _name = 'tbl_ops_plan'
#     _order = 'name desc'

   
#     tanggal = fields.Date('Tanggal', track_visibility='onchange', default=fields.Date.today())
#     user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user, readonly=True)
#     name = fields.Many2one('hr.employee','Employee', track_visibility='onchange')

class TBlWorkRequestDepartment(models.Model):
    _name = 'tbl_bisa_work_request_dept'
    _rec_name = 'nomor'

    nomor = fields.Char('Nomor', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    request_user = fields.Many2one('hr.employee','Request User')
    departement = fields.Many2one('hr.department','Departemen',related='request_user.department_id')
    unit_id = fields.Many2one('bisa_fleet.vehicle','Unit ID')
    task_id = fields.Many2one('tbl_bisa_hauling_assigment','Assignment ID')
    number = fields.Char('Number')
    hari = fields.Integer('Hari/Day')
    tanggal = fields.Date('Tanggal/Date', default=fields.Date.today())
    detail = fields.One2many('tbl_bisa_detail_wrd', 'data', 'Detail')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
    ], 'Status', default='draft')
    type = fields.Selection([
        ('preventive', 'Preventive'),
        ('breakdown', 'Breakdown'),
        ('scheduled', 'Scheduled'),
    ], 'Type', required=True)
    template = fields.Many2one('tbl_bisa_maintenance_template', 'Template')
    route = fields.Many2one('tbl_bisa_route','Route', related='task_id.route', store=True)
    lokasi = fields.Char('Location Unit')

    @api.model
    def create(self, vals):
        if vals.get('nomor', _('New')) == _('New'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_work_req_dept') or _('New')
        result = super(TBlWorkRequestDepartment, self).create(vals)
        return result

    def action_confirm(self):
        work_obj = self.env['tbl_bisa_work_request']
        work_detail_obj = self.env['tbl_bisa_job_out_line']
        work_part_detail_obj = self.env['tbl_bisa_maintenance_wr_template_detail']
        for rec in self:
            if rec.detail:
                data_detail = work_obj.create({
                            'tanggal': rec.tanggal,
                            'maintenance_type': 'repair_bd',
                            'unit_id': rec.unit_id.id,
                            'operator_driver': rec.request_user.id,
                            'task_id': rec.task_id.id,
                            'type': rec.type,
                            'lokasi': rec.lokasi,
                })
                # raise UserError(_('aaaaa'))
                for data in rec.detail:
                    data_detail_line = work_detail_obj.create({
                            'data_joline': data_detail.id,
                            'template': data.template.id,
                    })
                for data1 in rec.detail.template.detail:
                    data_detail_line_part = work_part_detail_obj.create({
                            'part_line': data_detail.id,
                            'part': data1.part.id,
                            'qty': data1.qty,
                            'uom': data1.uom.id,
                    })
                rec.state = 'confirm'

    # def onchange_date(self, cr, uid, ids, tanggal):
    #         res ={}       
    #         if tanggal :
    #             a = datetime.strptime(tanggal,"%Y-%m-%d")           
    #             if a :
    #                 b = datetime.strftime(a, '%A')               
    #                 res = {'hari': b }                
    #             return {'value': res}      
    #         return True

    # def _get_day(self):
    #     get_date = datetime.datetime.now().strftime('%A')

class TblDetailWrd(models.Model):
    _name = 'tbl_bisa_detail_wrd'
    
    template = fields.Many2one('tbl_bisa_maintenance_template', 'Template', required=True)
    description = fields.Char('Description')
    qty = fields.Integer('QTY')
    uom = fields.Char('UOM')
    remark = fields.Char('Remark')
    data = fields.Many2one('tbl_bisa_work_request_dept', 'Data')

class TblWorkRequest(models.Model):
    _name = 'tbl_bisa_work_request'
    _rec_name = 'nomor'

    nomor = fields.Char('Nomor', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    tgl_terbit = fields.Date('Tanggal Terbit', default=fields.Date.today())
    revisi = fields.Integer('Revisi')
    tanggal = fields.Date('Date/Tanggal', default=fields.Date.today())
    shift = fields.Selection([('siang', 'Siang'), ('malam', 'Malam')], 'Shift')
    maintenance_type = fields.Selection([
        ('repair_bd', 'Repair (B/D)'), 
        ('overhoul_oh', 'Overhoul (OH)'), 
        ('accident_acd', 'Accident (ACD)'),
    ], 'Maintenance Type')
    unit_id = fields.Many2one('bisa_fleet.vehicle','Unit ID')
    task_id = fields.Many2one('tbl_bisa_hauling_assigment','Assignment ID')
    operator_driver = fields.Many2one('hr.employee', 'Operator/Driver')
    hm_km = fields.Float('HM/KM')
    model = fields.Char('Model')
    time_start = fields.Datetime('Time Start/Jam Masuk')
    time_stop = fields.Datetime('Time Stop/Jam Keluar')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ready', 'Ready'),
        ('start', 'Start'), 
        ('pause', 'Pause'), 
        ('stop', 'Stop'), 
        ('done', 'Done'), 
    ], 'Status', default='draft')
    joline = fields.One2many('tbl_bisa_job_out_line', 'data_joline', 'Jo Line')
    maline = fields.One2many('tbl_bisa_mecanic_action_line', 'data_maline', 'Ma Line')
    partline = fields.One2many('tbl_bisa_maintenance_wr_template_detail', 'part_line', 'Part Line')
    type = fields.Selection([
        ('preventive', 'Preventive'),
        ('breakdown', 'Breakdown'),
        ('scheduled', 'Scheduled'),
    ], 'Type', required=True)
    route = fields.Many2one('tbl_bisa_route','Route', related='task_id.route', store=True)
    lokasi = fields.Char('Location Unit')

    @api.model
    def create(self, vals):
        if vals.get('nomor', _('New')) == _('New'):
                vals['nomor'] = self.env['ir.sequence'].next_by_code('seq_work_req') or _('New')
        result = super(TblWorkRequest, self).create(vals)
        return result


    def act_lanjutkan_assignment(self):
        if self.task_id:
            self.task_id.state = 'operasional'

    def act_stop_assignment(self):
        if self.task_id:
            self.task_id.state = 'cancel'

    def act_confirm(self):
        self.state = 'ready'

    def act_start(self):
        self.state = 'start'
        self.time_start = datetime.datetime.now()

    def act_pause(self):
        self.state = 'pause'

    def act_stop(self):
        self.state = 'stop'
        self.time_stop = datetime.datetime.now()

    def act_done(self):
        self.state = 'done'

    def act_ambil_part(self):
        a=1

    def act_purchase(self):
        a=1

    def act_cek_stock(self):
        a=1


class TblJobOutLine(models.Model):
    _name = 'tbl_bisa_job_out_line'

    job_out_line = fields.Char('Job Out Line/Jenis Kerusakan')
    template = fields.Many2one('tbl_bisa_maintenance_template', 'Template', required=True)
    data_joline = fields.Many2one('tbl_bisa_work_request', 'Data Job Out Line')
    state = fields.Selection([
        ('ok', 'OK'), 
        ('nok', 'Not OK'), 
    ], 'Status', default='nok')
    rem = fields.Char('Remarks')

class TblMecanicActionLine(models.Model):
    _name = 'tbl_bisa_mecanic_action_line'

    product = fields.Many2one('product.product','Mecanic Action Taken/Pekerjaan Mekanik')
    mecanic_action = fields.Char('Mecanic Action Taken/Pekerjaan Mekanik')
    time_progress_start = fields.Datetime('Start')
    time_progress_stop = fields.Float('Stop')
    time_progress_total = fields.Float('Total')
    mechanic_name = fields.Char('Mechanic Name')
    data_maline = fields.Many2one('tbl_bisa_work_request', 'Data Mechanic Line')
    rem = fields.Char('Remarks')

class TblBisaMaintenanceWrTemplateDetail(models.Model):
    _name = 'tbl_bisa_maintenance_wr_template_detail'

    part_line = fields.Many2one('tbl_bisa_work_request','Work Order')
    part = fields.Many2one('product.product', 'Part / Service')
    qty = fields.Integer('Qty')
    uom = fields.Many2one('uom.uom','UOM')
    rem = fields.Char('Remarks')
    lokasi = fields.Many2one('stock.location','Location')
    part_oh = fields.Float('On Hand')

class TblBisaMaintenanceTemplate(models.Model):
    _name = 'tbl_bisa_maintenance_template'

    name = fields.Char('Name') 
    unit_id = fields.Many2one('bisa_fleet.vehicle','Unit ID')
    detail = fields.One2many('tbl_bisa_maintenance_template_detail','details','Details')


class TblBisaMaintenanceTemplateDetail(models.Model):
    _name = 'tbl_bisa_maintenance_template_detail'

    details = fields.Many2one('tbl_bisa_maintenance_template','Details')
    part = fields.Many2one('product.product', 'Part / Service')
    qty = fields.Integer('Qty')
    uom = fields.Many2one('uom.uom','UOM')
    ket = fields.Char('Keterangan')

class TblBisaMaintenanceLocationDefault(models.Model):
    _name = 'tbl_bisa_maintenance_location_default' 

    name = fields.Many2one('stock.location','Location')

