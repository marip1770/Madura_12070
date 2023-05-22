# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class msi_hauling_users(models.Model):
    _inherit = 'res.users'

    # lokasi_id = fields.One2many('tbl_msi_lokasi','akses_ids','Site') 
    lokasi_id1 = fields.One2many('tbl_msi_lokasi','akses_ids','Site')
    project_id = fields.One2many('tbl_msi_projek','akses_ids', 'Project') 
    servis_id = fields.One2many('tbl_msi_servis','akses_ids', 'Servis') 
 
class tbl_msi_lokasi(models.Model):
    _name = 'tbl_msi_lokasi'
    _order = 'name'

    name = fields.Many2one('tbl_employee_lokasi','Site')
    akses_ids = fields.Many2one('res.users','User')

class tbl_msi_projek(models.Model):
    _name = 'tbl_msi_projek'
    _rec_name = 'project'

    project = fields.Many2one('project.project','Project')
    akses_ids = fields.Many2one('res.users','User')

class tbl_msi_servis(models.Model):
    _name = 'tbl_msi_servis'
    _rec_name = 'servis'

    servis = fields.Selection([
        ('hauling', 'Hauling'),
        ('hrm', 'HRM'),
        ('rental', 'Rental'),
        ('port', 'Port'),
        ('fuel_truck', 'Fuel Truck'),
        ('water_truck', 'Water Truck'),
        ('tls', 'TLS'),
    ], 'Servis')
    akses_ids = fields.Many2one('res.users','User')