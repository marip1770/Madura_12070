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

class tbl_msi_hr_structure(models.Model):
    _name = 'tbl_msi_hr_structure'
    _description = "tbl_msi_hr_structure"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char('Name')
    date = fields.Date('Date', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    ket = fields.Char('Keterangan')  
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    akses = fields.Selection([
        ('Direksi', 'Direksi'),
        ('GM', 'GM'),
        ('MGR', 'Manager'),
        ('STAFF', 'Staff'),
        ], string='Akses', default='STAFF')
    detail = fields.One2many('tbl_msi_hr_structure_detail','details','Detail')





class tbl_msi_hr_structure_detail(models.Model):
    _name = 'tbl_msi_hr_structure_detail'
    _description = "tbl_msi_hr_structure_detail"
    _order = 'seq'


    details = fields.Many2one('tbl_msi_hr_structure','Detail')
    name = fields.Many2one('tbl_payrol_item_struktur','Name')
    kode = fields.Char('Code', related='name.kode', store=True)
    tipe = fields.Selection([
        ('Deduction', 'Deduction'),
        ('Allowance', 'Allowance'),
        ], string='Tipe', related='name.tipe', store=True)
    seq = fields.Float('Seq', default=1)
 






class tbl_payrol_item_struktur(models.Model):
    _name = 'tbl_payrol_item_struktur'
    _description = "tbl_payrol_item_struktur"
    _order = 'tipe, name'



    name = fields.Char('Name', required=True)
    kode = fields.Char('Code', required=True)
    tipe = fields.Selection([
        ('Deduction', 'Deduction'),
        ('Allowance', 'Allowance'),
        ], string='Tipe', default='Allowance', required=True)
    account_id = fields.Many2one('account.account', string="Expense Account", required=True,)
    is_auto = fields.Boolean('Value Automatic', default=True)
    tipe_potongan = fields.Selection([
        ('AT', 'After Tax'),
        ('BT', 'Before Tax'),
        ('-', '-'),
        ], string='Tipe Potongan') 
    taxable = fields.Boolean('Taxable', default=True) 
    kategori_pendapatan = fields.Selection([
        ('REG', 'Regular'),
        ('IREG', 'IRegular'),
        ], string='Kategori Pendapatan', default='REG') 
    kode_import = fields.Char('Kode Import', required=True)

