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

class TblWizardAssigment(models.Model):
    _name = 'tbl_bisa_wizard_assigment'

    # @api.model
    # def _default_date(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_ids', [])
    #     data = self.env['tbl_bisa_hauling_plan'].browse(active_ids)
    #     return data.tanggal

    # @api.model
    # def _default_lokasi(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_ids', [])
    #     data = self.env['tbl_bisa_hauling_plan'].browse(active_ids)
    #     return data.lokasi

    # @api.model
    # def _default_no_projek(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_ids', [])
    #     data = self.env['tbl_bisa_hauling_plan'].browse(active_ids)
    #     return data.no_projek

    # @api.model
    # def _default_qty_rencana(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_ids', [])
    #     data = self.env['tbl_bisa_hauling_plan'].browse(active_ids)
    #     return data.quantity

    # @api.model
    # def _default_uom(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_ids', [])
    #     data = self.env['tbl_bisa_hauling_plan'].browse(active_ids)
    #     return data.uom

    # @api.model
    # def _default_tipe(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_ids', [])
    #     data = self.env['tbl_bisa_hauling_plan'].browse(active_ids)
    #     return data.tipe

    # tanggal = fields.Date('Tanggal', default=_default_date)
    tanggal = fields.Date('Tanggal')
    # lokasi = fields.Many2one('tbl_employee_lokasi', 'Lokasi', default=_default_lokasi)
    lokasi = fields.Many2one('tbl_employee_lokasi', 'Lokasi')
    # no_projek = fields.Many2one('project.project', 'No Project', default=_default_no_projek)
    no_projek = fields.Many2one('project.project', 'No Project')
    # qty_rencana = fields.Float('QTY Rencana', default=_default_qty_rencana)
    qty_rencana = fields.Float('QTY Rencana')
    qty_aktual = fields.Float('QTY Aktual')
    # uom = fields.Many2one('uom.uom', 'Satuan', default=_default_uom)
    uom = fields.Many2one('uom.uom', 'Satuan')
    # tipe = fields.Selection([
    #     ('hauling', 'Hauling'),
    #     ('hrm', 'HRM'),
    #     ('rental', 'Rental'),
    #     ('port', 'Port'),
    #     ('fuel_truck', 'Fuel Truck'),
    #     ('water_truck', 'Water Truck'),
    # ], 'Type', default=_default_tipe)
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
    ], 'Type')
    detail_assigment_line = fields.One2many('tbl_bisa_detail_assigment','detail_assigment','Detail Assigment Line')

    @api.model
    def get_schedule_um(self):
        plane = self.env['tbl_bisa_hauling_plan'].browse(self.env.context.get('active_ids'))
        detail_obj = self.env['tbl_bisa_detail_assigment']
        employee = self.env['tbl_msi_rekap_attendance'].search([('sc_date_a', '=', plane.tanggal)])
        # raise UserError(_(employee))
        if employee:
            for emp in employee:
                    # raise UserError(_('Data %s telah ada di assigment' % (emp.employee.name, )))
                    data_detail = detail_obj.create({
                        'driver': emp.employee.id,
                        'detail_assigment': self.id,
                    })
                    # self.detail_assigment_line.append((1, 0, {
                    #     'driver': emp.employee.id,
                    #     # 'type': bill.type,
                    #     # 'queue': bill.queue,
                    #     # 'amount': bill.amount,
                    #     # 'paid': bill.paid,
                    #     # 'paiddate': bill.paiddate,
                    #     # 'amount_paid': bill.amount_paid,
                    #     # 'kuitansi_number': bill.kuitansi_number,
                    #     # 'status': bill.status,
                    #     # 'status_payment': bill.status_payment,
                    #     # 'invoice': invoice.id
                    # }))

    def action_create_assigment(self):
        assigment_obj = self.env['tbl_bisa_hauling_assigment']
        p5m_obj = self.env['tbl_bisa_hauling_assigment_p5m_line']
        kesiapan_obj = self.env['tbl_bisa_hauling_assigment_kesiapan_line']
        p2h_obj = self.env['tbl_bisa_hauling_assigment_p2h_line']
        
        cari_driver = assigment_obj
        if self.detail_assigment_line:
            for dc in self.detail_assigment_line:
                rec = cari_driver.search([('driver','=',dc.driver.id),('tanggal','=',self.tanggal),('tipe','=',self.tipe)], limit=1)
                if rec:
                    raise UserError(_('Data %s telah ada di assigment' % (dc.driver.name, )))
                else:
                    data_assigment = assigment_obj.create({
                        'tanggal': self.tanggal, 
                        'no_projek': self.no_projek.id, 
                        'qty_rencana': self.qty_rencana,
                        'uom': self.uom.id,
                        'lokasi_asal': dc.lokasi_asal.id,
                        'lokasi_tujuan': dc.lokasi_tujuan.id,
                        'driver': dc.driver.id,
                        'unit_id': dc.unit_id.id,
                        # 'user_driver': dc.user_driver.id,
                        'tipe': self.tipe,
                    })

                    rec_p5m = self.env['tbl_bisa_hauling_p5m'].search([('tipe','=',self.tipe)], limit=1, order="id desc")
                    for p5m_tmpl in rec_p5m.data_p5m_line:
                        data_p5m_assigment = p5m_obj.create({
                            'field_pertanyaan_p5m': p5m_tmpl.pertanyaan_p5m,
                            'normal_value': p5m_tmpl.normal_value,
                            'assigment_line_p5m': data_assigment.id,
                        })

                    rec_kesiapan = self.env['tbl_bisa_hauling_kesiapan_bekerja'].search([('tipe','=',self.tipe)], limit=1, order="id desc")
                    for kesiapan_tmpl in rec_kesiapan.data_kesiapan_line:
                        data_kesiapan_assigment = kesiapan_obj.create({
                            'field_pertanyaan_kesiapan': kesiapan_tmpl.pertanyaan_kesiapan,
                            'normal_value': kesiapan_tmpl.normal_value,
                            'assigment_line_kesiapan': data_assigment.id,
                        })

                    rec_p2h = self.env['tbl_bisa_hauling_p2h'].search([('tipe','=',self.tipe),('tipe_unit','=',dc.unit_id.tipe)], limit=1, order="id desc")
                    for p2h_tmpl in rec_p2h.data_p2h_line:
                        data_p2h_assigment = p2h_obj.create({
                            'field_pertanyaan_p2h': p2h_tmpl.pertanyaan_p2h,
                            'normal_value': p2h_tmpl.normal_value,
                            'assigment_line_p2h': data_assigment.id,
                        })

class TblDetailAssigment(models.Model):
    _name = 'tbl_bisa_detail_assigment'

    driver = fields.Many2one('hr.employee','Driver')
    unit_id = fields.Many2one('bisa_fleet.vehicle','Unit ID')
    lokasi_asal = fields.Many2one('tbl_employee_lokasi','Lokasi Asal')
    lokasi_tujuan = fields.Many2one('tbl_employee_lokasi','Lokasi Tujuan')
    tipe = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
    ], 'Type')
    detail_assigment = fields.Many2one('tbl_bisa_wizard_assigment', 'Detail Assigment')
