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



class tbl_msi_master_route(models.Model):
    _name = 'tbl_msi_master_route'

   
    name = fields.Char('Nama Route', required=True)
    asal = fields.Many2one('tbl_msi_lokasi','Asal', required=True)
    tujuan = fields.Many2one('tbl_msi_lokasi','Tujuan', required=True)
    rate = fields.Float('Rate')


class tbl_msi_master_transport(models.Model):
    _name = 'tbl_msi_master_transport'

    name = fields.Char('Jenis Truck', required=True)
    rate = fields.Float('Rate')

class tbl_msi_lokasi(models.Model):
    _name = 'tbl_msi_lokasi'

    name = fields.Char('Lokasi', required=True)

class tbl_msi_driver_position(models.Model):
    _name = 'tbl_msi_driver_position'
   
    name = fields.Many2one('hr.employee', 'Nama Driver', required=True)
    nik = fields.Char('NIK', related='name.nik', store=True)
    id_employee = fields.Integer('ID Nama Driver', related='name.id', store=True)
    position = fields.Many2one('hr.job','Position')
    rate = fields.Float('Rate')

    @api.onchange('name')
    def _compute_employee(self):
        if self.name:
            self.position = self.name.job_id