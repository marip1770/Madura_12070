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
import math

class tbl_msi_payroll_tax(models.Model):
    _name = 'tbl_msi_payroll_tax'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char('Name', compute="_compute_nama", store=True)
    date = fields.Date('Date', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    periode = fields.Many2one('tbl_tax_period','Period') 
    ket = fields.Char('Keterangan')  
    state = fields.Selection([
        ('draft', 'Draft'),
        ('hitung1', 'Hitung'),
        ('hitung2', 'Hitung'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ('final', 'Final'),
        ('done', 'Done'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    detail = fields.One2many('tbl_msi_payroll_tax_line','details','Detail')


    @api.one
    @api.depends('periode','ket')
    def _compute_nama(self):
        if self.periode and self.ket:
           self.name = 'TAX' + ' ' + str(self.periode.name).upper() + ' ' +str(self.ket).upper()
        if self.periode and not self.ket:
           self.name = 'TAX' + ' ' + str(self.periode.name).upper()
        if not self.periode and self.ket:
           self.name = 'TAX' + ' ' + str(self.ket).upper()


    @api.one
    def action_submit(self):
        self.state = 'approve'

    @api.one
    def action_closing(self):
        self.state = 'done'


    @api.one
    def action_approve(self):
        for emp in self.detail:
            emp.action_approve()
        self.state = 'final'


    @api.one
    def action_gross(self):
        for emp in self.detail:
            emp.action_hitung()
            self.state = 'hitung2'


    @api.one
    def action_grossup(self):
        for emp in self.detail:
            emp.action_hitung()
            self.state = 'submit'


    @api.one
    def action_ulang(self):
        self.env.cr.execute("DELETE from tbl_msi_payroll_tax_line where details = %s",(self.id,))
        self.state = 'draft'



    @api.one
    def action_get(self):
        self.state = 'hitung1'
        proses_tax_obj = self.env['tbl_msi_payroll_tax_line']
        reg=0
        ireg=0
        bt=0
        self.env.cr.execute('select details, employee from tbl_msi_tax_input where payroll_date >= %s and payroll_date = %s group by details, employee', (self.periode.date_awal, self.periode.date_akhir))
        for hasil in self.env.cr.fetchall():
            self.env.cr.execute('select sum(nominal) from tbl_msi_tax_input where tipe = %s and kode =%s and details = %s and payroll_date >= %s and payroll_date = %s', ('Allowance','REG', hasil[0], self.periode.date_awal, self.periode.date_akhir))
            for hasil1 in self.env.cr.fetchall():
                reg=hasil1[0]

            self.env.cr.execute('select sum(nominal) from tbl_msi_tax_input where tipe = %s and kode =%s and details = %s and payroll_date >= %s and payroll_date = %s', ('Allowance','IREG', hasil[0], self.periode.date_awal, self.periode.date_akhir))
            for hasil3 in self.env.cr.fetchall():
                ireg=hasil3[0]

            self.env.cr.execute('select sum(nominal) from tbl_msi_tax_input where tipe_potongan = %s and details = %s and payroll_date >= %s and payroll_date = %s', ('BT',hasil[0], self.periode.date_awal, self.periode.date_akhir))
            for hasil2 in self.env.cr.fetchall():
                bt=hasil2[0]
            cari = self.env['hr.employee'].search([('name', '=', hasil[1])], order="id desc", limit=1)
            if cari:
                  bulan_mulai=0
                  tgl_mulai=0
                  nik=0
                  depan=''
                  tengah=''
                  blkg=''
                  if not cari.tgl_mulai:
                      raise UserError(_(("%s tidak ada tanggal mulai bekerja") % (cari.name)))
                        
                  tahun = self.periode.date_akhir.year - cari.tgl_mulai.year
                  tgl = self.periode.date_akhir - cari.tgl_mulai
                  nik = cari.nik
                  depan = cari.nama_depan
                  tengah = cari.nama_tengah or ''
                  blkg = cari.nama_belakang or ''
                  if tahun > 0:
                     bulan_mulai = 1
                     tgl_mulai=1
                  else:
                     bulan_mulai = cari.tgl_mulai.month
                     if tgl.days > 30:
                        tgl_mulai=1
                     else:                        
                        tgl_mulai= cari.tgl_mulai.day                    

                  data_line2 = proses_tax_obj.create({
                      'details': self.id,
                      'details_id': hasil[0],
                      'ptkp': cari.ptkp.id,
                      'value_ptkp': cari.ptkp.value,
                      'npwp': cari.npwp,
                      'gross': cari.gross,
                      'start_date': tgl_mulai,
                      'start_month': bulan_mulai,
                      'mopp': self.periode.date_akhir.month,
                      'ret': reg,
                      'iret': ireg,
                      'ptd': bt,
                      'periode': self.periode.id,
                      'tahun': self.periode.tahun.id,
                      'employee': str(depan) + ' ' + str(tengah) + ' ' + str(blkg),
                      'nik': nik,
                  })                      
             
class tbl_msi_payroll_tax_line(models.Model):
    _name = 'tbl_msi_payroll_tax_line'
    _order = 'details_id'

    details = fields.Many2one('tbl_msi_payroll_tax','Detail')
    details_id = fields.Char('Salary Id', help='Salary Id Header')
    periode = fields.Many2one('tbl_tax_period','Period')
    tahun = fields.Many2one('tbl_tax_year','Tahun')
    employee = fields.Char('Employee',)
    nik = fields.Char('NIK')
    gaji_temp = fields.Float('Gaji Temp', help='Sementara sebelum dialokasikan ke gross / gross up')
    gross = fields.Boolean('Is Gross')
    ptkp = fields.Many2one('tbl_employee_ptkp','PTKP', help='PTKP')
    value_ptkp = fields.Float('Value PTKP', help='Value PTKP')
    npwp = fields.Boolean('NPWP', help='Have NPWP?')
    tax_penalty = fields.Float('Tax Penalty', help='Tax Penalty', default=120)  
    start_date = fields.Float('Start Date', help='Start Date') 
    start_month = fields.Float('Start Month', help='Start Month') 
    mopp = fields.Float('Month of Pay Period', help='Month of Pay Period')

    af = fields.Float('Annualisation Factor', help='Annualisation Factor')  
    cpt = fields.Float('Current Period Tax', help='Current Period Tax') 
    er = fields.Float('Exchange Rate', help='Exchange Rate', default=1) 
    er_value = fields.Float('Exchange Rate  Value', help='Exchange Rate  Value') 

    ret = fields.Float('Regular Earning Total', help='Regular Earning Total') 
    rget = fields.Float('Regular GrossUp Earning Total', help='Regular GrossUp Earning Total') 
    rgta = fields.Float('Regular GrossUp Tax Allowance', help='Regular GrossUp Tax Allowance') 
    iret = fields.Float('IRegular Earning Total', help='IRegular Earning Total')
    irget = fields.Float('IRegular GrossUp Earning Total', help='IRegular GrossUp Earning Total') 
    irgta = fields.Float('IRegular GrossUp Tax Allowance', help='IRegular GrossUp Tax Allowance') 
    ptd = fields.Float('Pre Tax Deduction', help='Pre Tax Deduction') 


    annual_r = fields.Float('Annual R', help='Annual R')
 
    adpadec = fields.Float('Astek&DPA Deduction', help='Astek&DPA Deduction')
    max_pr = fields.Float('Max Pos Rebate', help='Max Pos Rebate')
    max_pran = fields.Float('Max Pos Rebate (Annual)', help='Max Pos Rebate (Annual)')
    min_pr = fields.Float('Min Pos Rebate', help='Min Pos Rebate')
    pos_reb = fields.Float('Position Rebate', help='Position Rebate')

    annual_net_r = fields.Float('Annual Net R', help='Annual Net R') 

    net_taxr = fields.Float('Net Tax R', help='Net Taxable R')

    annrtax = fields.Float('Annual R Tax', help='Annual R Tax')
    annrtaxap = fields.Float('Annual R Tax After Penalty', help='Annual R Tax After Penalty')
    cprtax = fields.Float('Current Period R Tax', help='Current Period R Tax')
    annrig = fields.Float('Annual RIG', help='Annual R I G')

    adpadec1 = fields.Float('Astek&DPA Deduction', help='Astek&DPA Deduction')
    max_pr1 = fields.Float('Max Pos Rebate', help='Max Pos Rebate')
    max_pran1 = fields.Float('Max Pos Rebate (Annual)', help='Max Pos Rebate (Annual)')
    min_pr1 = fields.Float('Min Pos Rebate', help='Min Pos Rebate')
    pos_reb1 = fields.Float('Position Rebate', help='Position Rebate')

    netrig = fields.Float('Net RIG', help='Net R I G')
    netaxrig = fields.Float('Net Taxable RIG', help='Net Taxable R I G')
 
    annrigtax = fields.Float('Annual RIG Tax', help='Annual R I G Tax')
    annrigtaxap = fields.Float('Annual RIG Tax After Penalty', help='Annual R I G Tax After Penalty')
    anngtax = fields.Float('Annual G Tax', help='Annual G Tax')
    cpgtax = fields.Float('Current Period G Tax', help='Current Period G Tax')
    rigtax = fields.Float('RIG TAx', help='R I G Tax')
    annri = fields.Float('Annual R + I', help='Annual R + I')

    adpadec2 = fields.Float('Astek&DPA Deduction', help='Astek&DPA Deduction')
    max_pr2 = fields.Float('Max Pos Rebate', help='Max Pos Rebate')
    max_pran2 = fields.Float('Max Pos Rebate (Annual)', help='Max Pos Rebate (Annual)')
    min_pr2 = fields.Float('Min Pos Rebate', help='Min Pos Rebate')
    pos_reb2 = fields.Float('Position Rebate', help='Position Rebate')
   
    net_ri = fields.Float('Net R + I', help='Net R + I')
    
    net_taxri = fields.Float('Net Taxable R + I', help='Net Taxable R + I')
    
    annual_ritax = fields.Float('Annual R + I Tax', help='Annual R + I Tax')
    annual_ritax_ap = fields.Float('Annual R + I Tax After Penalty', help='Annual R + I Tax After Penalty')
    cp_itax = fields.Float('Current Period I Tax', help='Current Period I Tax')

    ri_taxded = fields.Float('R & I  Tax Deduction', help='R & I  Tax Deduction')

    c_et = fields.Float('C Earning Total', help='C Earning Total')
    c_ta = fields.Float('C Tax Allowance (until = B85)', help='C Tax Allowance (until = B85)')

    annual_rige = fields.Float('Annual R, I, G, & E', help='Annual R, I, G, & E')

    net_rige = fields.Float('Net R, I, G, & E', help='Net R, I, G, & E')

    adpadec3 = fields.Float('Astek&DPA Deduction', help='Astek&DPA Deduction')
    max_pr3 = fields.Float('Max Pos Rebate', help='Max Pos Rebate')
    max_pran3 = fields.Float('Max Pos Rebate (Annual)', help='Max Pos Rebate (Annual)')
    min_pr3 = fields.Float('Min Pos Rebate', help='Min Pos Rebate')
    pos_reb3 = fields.Float('Position Rebate', help='Position Rebate')

    net_taxrige = fields.Float('Net Taxable R, I, G, & E', help='Net Taxable R, I, G, & E')

    annual_rigetax = fields.Float('Annual R, I, G, & E Tax', help='Annual R, I, G, & E Tax')
    annual_rigetax_ap = fields.Float('Annual R, I, G, & E Tax After Pen', help='Annual R, I, G, & E Tax After Pen')
    e_tax = fields.Float('E Tax', help='E Tax')

    rige_taxded = fields.Float('R, I, G, & E Tax Deduction', help='R, I, G, & E Tax Deduction')
    
    tax_allow = fields.Float('Tax Allowance', help='Tax Allowance')
    employee_tax = fields.Float('Employee Tax', help='Employee Tax')
    
    total_tpty = fields.Float('Total Tax Paid This Year', help='Total Tax Paid This Year')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ], string='Status', default='draft')


    @api.one
    def action_hitung(self):
      if not self.nik:
         raise UserError(_(("%s tidak ada nik") % (self.employee)))

      af=0
      cpt=0
      pos_reb=0
      exp=3
      tot_earn=0
      tot_ptd=0
      tot_etax=0
      tot_c_et=0
      tot_c_ta=0
      tot_cp_itax=0
      tot_iret=0
      tot_cpgtax=0
      tot_rget=0
      tot_rgta=0
      tot_cprtax=0
      self.env.cr.execute('select sum(ret), sum(ptd), sum(e_tax), sum(c_et), sum(c_ta), sum(cp_itax), sum(iret), sum(cpgtax), sum(rget), sum(rgta), sum(cprtax) from tbl_msi_payroll_tax_line where tahun = %s and nik = %s and state = %s', (self.tahun.id, self.nik, 'submit'))
      hasil = self.env.cr.fetchall()
      if hasil:
         for hasil1 in hasil:
             if hasil1[0]:
                tot_earn = hasil1[0]
             if hasil1[1]:
                tot_ptd = hasil1[1]
             if hasil1[2]:
                tot_etax = hasil1[2]
             if hasil1[3]:
                tot_c_et = hasil1[3]
             if hasil1[4]:
                tot_c_ta = hasil1[4]
             if hasil1[5]:
                tot_cp_itax = hasil1[5]
             if hasil1[6]:
                tot_iret = hasil1[6]
             if hasil1[7]:
                tot_cpgtax = hasil1[7]
             if hasil1[8]:
                tot_rget = hasil1[8]
             if hasil1[9]:
                tot_rgta = hasil1[9]
             if hasil1[10]:
                tot_cprtax = hasil1[10]

      ########## Gross
      ####raise UserError(_(("tahun: %s") % (self.nik)))
      if self.employee:
        self.rget = 0
        i=0
        while i != 1:
           ###### Annualisation Factor
           af = (30*(13 - self.start_month) - self.start_date + 1)/(30*(self.mopp - self.start_month + 1) - self.start_date + 1)
           self.af = af

           self.cpt = round(self.rige_taxded)

           if self.cpt == 0:
              cpt=0
           else:
              cpt=self.cpt / self.er

           self.er_value = cpt
           self.annual_r = round((tot_earn + self.ret) * self.af)
           self.adpadec = round((tot_ptd + self.ptd) * -self.af)




           self.max_pr = round(500000 * (self.mopp - self.start_month + 1))


           self.max_pran = round(self.max_pr * self.af)
           self.min_pr = round((5/100)  * self.annual_r)

           if self.min_pr < self.max_pran:
              pos_reb = -self.min_pr
           else:
              pos_reb = -self.max_pran

           self.pos_reb = pos_reb
           self.annual_net_r = round(self.annual_r + self.adpadec + self.pos_reb)
           self.net_taxr = int(math.floor((((self.annual_net_r - self.value_ptkp)/1000)*1000)/10**exp) * 10**exp)

           annrtax=0
           if self.net_taxr > 500000000:
               annrtax = self.net_taxr * 0.3 - 55000000
           else:
               if self.net_taxr > 250000000:
                  annrtax = self.net_taxr * 0.25 - 30000000
               else:
                  if self.net_taxr > 50000000:
                     annrtax = self.net_taxr * 0.15 - 5000000
                  else:
                     if self.net_taxr > 0:
                        annrtax = self.net_taxr * 0.05
   
           self.annrtax = round(annrtax)

           annrtaxap=0
           if self.npwp:
              annrtaxap = self.annrtax
           else:
              annrtaxap = self.annrtax * (self.tax_penalty/100)

           self.annrtaxap = round(annrtaxap)
           self.cprtax = round((self.annrtaxap /af) - tot_cprtax)

           self.annrig = round(((tot_earn + tot_rget + tot_rgta + self.ret + self.rget + self.rgta ) * af ) + (tot_iret + self.iret))

           #####
           self.adpadec1 = self.adpadec
           self.max_pr1 =  round(500000 * (self.mopp - self.start_month + 1))
           self.max_pran1 = round(self.max_pr1 * self.af)
           self.min_pr1 = round((5/100)  * self.annrig)
           if self.min_pr1 < self.max_pran1:
              pos_reb1 = -self.min_pr1
           else:
              pos_reb1 = -self.max_pran1
           self.pos_reb1 = pos_reb1
           #####

           self.netrig  = self.annrig + self.adpadec1 + self.pos_reb1
           self.netaxrig  = int(math.floor((((self.netrig - self.value_ptkp)/1000)*1000)/10**exp) * 10**exp)

           annrigtax=0
           if self.netaxrig > 500000000:
               annrigtax = self.netaxrig * 0.3 - 55000000
           else:
               if self.netaxrig > 250000000:
                  annrigtax = self.netaxrig * 0.25 - 30000000
               else:
                  if self.netaxrig > 50000000:
                     annrigtax = self.netaxrig * 0.15 - 5000000
                  else:
                      if self.netaxrig > 0:
                         annrigtax = self.netaxrig * 0.05
   
           self.annrigtax = annrigtax

           annrigtaxap=0
           if self.npwp:
              annrigtaxap = self.annrigtax
           else:
              annrigtaxap = self.annrigtax * (self.tax_penalty/100)

           self.annrigtaxap = annrigtaxap
           self.anngtax = self.annrigtaxap - self.annual_ritax_ap


           self.cpgtax = (self.anngtax / self.af) - tot_cpgtax


           self.rigtax = self.cpgtax + self.ri_taxded


           self.annri = ((tot_earn + self.ret) * self.af) + (self.iret + tot_iret)

           #####
           self.adpadec2 = self.adpadec1
           self.max_pr2 =  round(500000 * (self.mopp - self.start_month + 1))
           self.max_pran2 = round(self.max_pr2 * self.af)
           self.min_pr2 = round((5/100)  * self.annri)
           if self.min_pr2 < self.max_pran2:
              pos_reb2 = -self.min_pr2
           else:
              pos_reb2 = -self.max_pran2
           self.pos_reb2 = pos_reb2
           #####


           self.net_ri = int(math.floor((self.annri + self.adpadec2 + self.pos_reb2)/10**exp) * 10**exp)


           self.net_taxri = ((self.net_ri - self.value_ptkp)/1000) * 1000

           annual_ritax=0
           if self.net_taxri > 500000000:
               annual_ritax = self.net_taxri * 0.3 - 55000000
           else:
               if self.net_taxri > 250000000:
                  annual_ritax = self.net_taxri * 0.25 - 30000000
               else:
                  if self.net_taxri > 50000000:
                      annual_ritax = self.net_taxri * 0.15 - 5000000
                  else:
                      if self.net_taxri > 0:
                         annual_ritax = self.net_taxri * 0.05

           self.annual_ritax = annual_ritax

           annual_ritax_ap=0
           if self.npwp:
              annual_ritax_ap = self.annual_ritax
           else:
              annual_ritax_ap = self.annual_ritax * (self.tax_penalty/100)

           self.annual_ritax_ap = annual_ritax_ap

           self.cp_itax = self.annual_ritax_ap - self.annrtaxap - tot_cp_itax
           self.ri_taxded = self.cp_itax + self.cprtax
           self.c_et = self.irget
           self.c_ta = self.irgta
           self.annual_rige = self.annrig + self.c_et + self.c_ta + tot_c_et + tot_c_ta 

           #####
           self.adpadec3 = self.adpadec2
           self.max_pr3 =  round(500000 * (self.mopp - self.start_month + 1))
           self.max_pran3 = round(self.max_pr3 * self.af)
           self.min_pr3 = round((5/100)  * self.annual_rige)
           if self.min_pr3 < self.max_pran3:
              pos_reb3 = -self.min_pr3
           else:
              pos_reb3 = -self.max_pran3
           self.pos_reb3 = pos_reb3
           #####
      
           self.net_rige = self.annual_rige + self.adpadec3 + self.pos_reb3

           self.net_taxrige = int(math.floor((((self.net_rige - self.value_ptkp)/1000) * 1000)/10**exp) * 10**exp)

           annual_rigetax=0
           if self.net_taxrige > 500000000:
               annual_rigetax = self.net_taxrige * 0.3 - 55000000
           else:
               if self.net_taxrige > 250000000:
                  annual_rigetax = self.net_taxrige * 0.25 - 30000000
               else:
                  if self.net_taxrige > 50000000:
                      annual_rigetax = self.net_taxrige * 0.15 - 5000000
                  else:
                      if self.net_taxrige > 0:
                         annual_rigetax = self.net_taxrige * 0.05

           self.annual_rigetax = annual_rigetax

           annual_rigetax_ap=0
           if self.npwp:
              annual_rigetax_ap = self.annual_rigetax
           else:
              annual_rigetax_ap = self.annual_rigetax * (self.tax_penalty/100)

           self.annual_rigetax_ap = annual_rigetax_ap
           self.e_tax = self.annual_rigetax_ap - self.annrigtaxap - tot_etax
           self.rige_taxded = self.e_tax + self.rigtax       
           self.tax_allow = self.e_tax + self.cpgtax
           self.employee_tax = self.cp_itax  + self.cprtax
           i = i+1
        

    @api.one
    def action_approve(self):
        cari = self.env['tbl_msi_payroll_line'].search([('id', '=', int(self.details_id))], order="id desc", limit=1)
        if cari: 
           if self.gross:
#             raise UserError(_(("%s , %s") % (self.employee_tax, cari)))

            #   cari.total_tax = self.employee_tax
              cari.total_tunj_tax = self.employee_tax
           else:
             cari.total_tax = self.employee_tax
           cari.tax_siap = True
        self.state = 'submit'



