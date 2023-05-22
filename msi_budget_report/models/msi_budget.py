# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import email_re, email_split, email_escape_char, float_is_zero, float_compare, \
    pycompat, date_utils
from odoo.exceptions import UserError, AccessError
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from calendar import monthrange

import math


class tbl_msi_budget(models.Model):
    _name = "tbl_msi_budget"

    tahun = fields.Many2one('tbl_msi_budget_tahun','Tahun', required=True)
    bulan = fields.Selection([
        ('1', 'Januari'),
        ('2', 'Februari'),
        ('3', 'Maret'),
        ('4', 'April'),
        ('5', 'Mei'),
        ('6', 'Juni'),
        ('7', 'Juli'),
        ('8', 'Agustus'),
        ('9', 'September'),
        ('10', 'Oktober'),
        ('11', 'Nopember'),
        ('12', 'Desember'),
        ], 'Bulan', default='1', required=True)
    detail = fields.One2many('tbl_msi_budget_detail','details','Detail Budget')

    @api.multi
    def action_get(self):
        analitik_obj = self.env['crossovered.budget.lines']
        report_line_obj = self.env['tbl_msi_budget_detail']
        tgl_awal = str(self.tahun.name)+'-01-01'
        tgl_akhir = str(self.tahun.name)+'-12-31'
        if self.detail:
                 self.detail.unlink()

        analitik = analitik_obj.search([('date_from', '=', str(tgl_awal)),('date_to', '=', str(tgl_akhir))],)
        if analitik:
           for hasil in analitik:
              #raise UserError(_(hasil.planned_amount))
              budget_bulan=0
              if hasil.planned_amount > 0:
                 budget_bulan = hasil.planned_amount / 12
              ytd_bulan=0
              if hasil.planned_amount > 0:
                 ytd_bulan = (hasil.planned_amount / 12) * int(self.bulan)
              bulan_aktual1=0
              bulan_aktual_ytd=0
              bulan_aktual_tahun=0
              for akun in hasil.general_budget_id.account_ids:
                 num_days = monthrange(int(self.tahun.name), int(self.bulan))[1]
                 #raise UserError(_(num_days))
                 tgl_awal_bulan = str(self.tahun.name)+'-'+str(self.bulan)+'-01'
                 tgl_awal_bulan_ytd = str(self.tahun.name)+'-01-01'
                 tgl_akhir_bulan = str(self.tahun.name)+'-'+str(self.bulan)+'-'+str(num_days)
                 tgl_akhir_bulan_tahun = str(self.tahun.name)+'-'+str(self.bulan)+'-'+str(num_days)
                 #raise UserError(_(hasil.analytic_account_id.id))

                 self.env.cr.execute("select debit, credit \
                      from account_move_line \
                      where date >= %s and \
                      date <= %s and \
                      analytic_account_id = %s and \
                      account_id = %s", (str(tgl_awal_bulan),str(tgl_akhir_bulan),hasil.analytic_account_id.id,akun.id))
                 akun1 = self.env.cr.fetchall()
                 #raise UserError(_(akun1))
                 for hasil_akun1 in akun1:
                     bulan_aktual1 += (hasil_akun1[0] + hasil_akun1[1])

                 self.env.cr.execute("select debit, credit \
                      from account_move_line \
                      where date >= %s and \
                      date <= %s and \
                      analytic_account_id = %s and \
                      account_id = %s", (str(tgl_awal_bulan_ytd),str(tgl_akhir_bulan),hasil.analytic_account_id.id,akun.id))
                 akun1 = self.env.cr.fetchall()
                 #raise UserError(_(akun1))
                 for hasil_akun1 in akun1:
                     bulan_aktual_ytd += (hasil_akun1[0] + hasil_akun1[1])

                 self.env.cr.execute("select debit, credit \
                      from account_move_line \
                      where date >= %s and \
                      date <= %s and \
                      analytic_account_id = %s and \
                      account_id = %s", (str(tgl_awal_bulan_ytd),str(tgl_akhir_bulan_tahun),hasil.analytic_account_id.id,akun.id))
                 akun1 = self.env.cr.fetchall()
                 #raise UserError(_(akun1))
                 for hasil_akun1 in akun1:
                     bulan_aktual_tahun += (hasil_akun1[0] + hasil_akun1[1])
              persen_bulan = 0
              persen_ytd = 0
              persen_tahun = 0
              if budget_bulan > 0 and bulan_aktual1 > 0:
                 persen_bulan = (bulan_aktual1 / budget_bulan) * 100
              if ytd_bulan > 0 and bulan_aktual_ytd > 0:
                 persen_ytd = (bulan_aktual_ytd / ytd_bulan) * 100
              if hasil.planned_amount > 0 and bulan_aktual_tahun > 0:
                 persen_tahun = (bulan_aktual_tahun / hasil.planned_amount) * 100

                 
              data_line2 = report_line_obj.create({
                  'details': self.id,
                  'budget': hasil.id,
                  'tahun_budget': hasil.planned_amount or 0,
                  'bulan_budget': budget_bulan,
                  'y2d_budget': ytd_bulan,
                  'bulan_aktual': bulan_aktual1,
                  'y2d_aktual': bulan_aktual_ytd,
                  'tahun_aktual': bulan_aktual_tahun,
                  'bulan_budget_persen': persen_bulan,
                  'y2d_budget_persen': persen_ytd,
                  'tahun_budget_persen': persen_tahun,
             })


class tbl_msi_budget_detail(models.Model):
    _name = "tbl_msi_budget_detail"

    details = fields.Many2one('tbl_msi_budget','Budget')
    budget = fields.Many2one('crossovered.budget.lines','Nama Budget')
    bulan_budget = fields.Float('Budget bulan')
    bulan_aktual = fields.Float('Budget aktual ')
    bulan_varian = fields.Float('Budget varian ',compute="_compute_bulan_varian")
    bulan_budget_persen = fields.Float('Persentase')
    spasi = fields.Char(' ', readonly=True)
    y2d_budget = fields.Float('Y2d bulan')
    y2d_aktual = fields.Float('Y2d aktual ')
    y2d_varian = fields.Float('Y2d varian ',compute="_compute_y2d_varian")
    y2d_budget_persen = fields.Float('Persentase')
    spasi = fields.Char(' ', readonly=True)
    tahun_budget = fields.Float('Budget Tahun')
    tahun_aktual = fields.Float('Budget Tahun Aktual ')
    tahun_varian = fields.Float('Budget Tahun varian ',compute="_compute_tahun_varian")
    tahun_budget_persen = fields.Float('Persentase')

    @api.one
    @api.depends('bulan_budget','bulan_aktual')
    def _compute_bulan_varian(self):
            self.bulan_varian = self.bulan_budget-self.bulan_aktual

    @api.one
    @api.depends('y2d_budget','y2d_aktual')
    def _compute_y2d_varian(self):
            self.y2d_varian = self.y2d_budget-self.y2d_aktual

    @api.one
    @api.depends('tahun_budget','tahun_aktual')
    def _compute_tahun_varian(self):
            self.tahun_varian = self.tahun_budget-self.tahun_aktual




class tbl_msi_budget_tahun(models.Model):
    _name = "tbl_msi_budget_tahun"

    name = fields.Char('Name')


