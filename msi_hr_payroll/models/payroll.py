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

class tbl_msi_payroll_bulanan(models.Model):
    _name = 'tbl_msi_payroll_bulanan'
    _description = "Payroll BUlanan"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char('Name', compute="_compute_nama", store=True)
    date = fields.Date('Date', default=fields.Date.today())
    tahun = fields.Integer('Tahun', required=True)
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    periode = fields.Many2one('tbl_payroll_period','Period', required=True)  
    ket = fields.Char('Keterangan') 
    state = fields.Selection([
        ('draft', 'Draft'),
        ('data', 'Data'),
        ('proses', 'Proses'),
        ('tax_send', 'Proses Pajak'),
        ('tax_receive', 'Cek Pajak'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ('close', 'Closed'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    source = fields.Selection([
        ('raw', 'Data Raw'),
        ('import', 'Data Import'),
        ], string='Source', required=True)

    tipe = fields.Selection([
        ('regular', 'Regular'),
        ('adhoc', 'Adhoc'),
        ('exit', 'Exit'),
        ], string='Tipe', required=True, default='regular')

    tipe_proses = fields.Selection([
        ('all', 'ALL'),
        ('department', 'Department'),
        ('struktur', 'Struktur Payroll'),
        ], string='Tipe Proses', required=True, default='all')
    dept = fields.Many2one('hr.department', 'Department')
    struktur_gaji = fields.Many2one("tbl_msi_hr_structure", string="Strukture Payroll")
    detail = fields.One2many('tbl_msi_payroll_line','details','Detail')

    file_import = fields.Binary("Import 'csv' Manual Input", help="*Import a list of lot/serial numbers from a csv file \n *Only csv files is allowed"
                                                          "\n *The csv file must contain a row header namely 'Serial Number'")
    file_name = fields.Char("file name")

    #     importing "csv" file and appending the datas from file to order lines
    @api.multi
    def input_file(self):
        if self.file_import_ri:
            move_line_obj = sn_obj = self.env['stock.move.line']
            file_value = self.file_import_ri.decode("utf-8")
            filename, FileExtension = os.path.splitext(self.file_name_ri)
            if FileExtension != '.csv':
                raise UserError("Invalid File! Please import the 'csv' file")
            csv_data = base64.b64decode(file_value)
            data_file = io.StringIO(csv_data.decode("utf-8"))
            data_file.seek(0)
            file_reader = []
            csv_reader = csv.reader(data_file, delimiter=',')
            csv_reader1 = csv.reader(data_file, delimiter=',')
            aa=0
            #raise UserError(_("lanjut"))
            if self.move_line_ids:
               self.move_line_ids.unlink()
            for row in csv_reader:
                try:
                   if row[0] != 'serial':
                      aa = aa + int(row[1])
                      data = self.env['stock.production.lot'].search([('product_id', '=', self.product_id.id), ('name', '=', str(row[0].strip()))])
                      if data:
                        raise UserError(_('Serial Number %s  Sudah Ada') % (row[0],))
                      else:
                        if row[2]:
                          #raise UserError(_('uom %s  Sudah Ada') % (self.product_uom.id,))
                          data_line21 = move_line_obj.create({
                             'move_id': self.id,
                             'product_id': self.product_id.id,
                             'lot_name': row[0].strip(),
                             'expired_date': row[2].strip(),
                             'qty_done': int(row[1].strip()),
                             'product_qty': int(row[1].strip()),
                             'product_uom_qty': int(row[1].strip()),
                             'product_uom_id': self.product_uom.id,
                             'location_id': self.location_id.id,
                             'location_dest_id': self.location_dest_id.id,
                             'picking_id': self.picking_id.id,
                          })
                        else:
                          #raise UserError(_('uom %s  Sudah Ada') % (self.product_uom.id,))
                          data_line21 = move_line_obj.create({
                             'move_id': self.id,
                             'product_id': self.product_id.id,
                             'lot_name': row[0].strip(),
                             #'expired_date': row[2].strip(),
                             'qty_done': int(row[1].strip()),
                             'product_qty': int(row[1].strip()),
                             'product_uom_qty': int(row[1].strip()),
                             'product_uom_id': self.product_uom.id,
                             'location_id': self.location_id.id,
                             'location_dest_id': self.location_dest_id.id,
                             'picking_id': self.picking_id.id,
                          })

                except Exception:
                   continue

            if aa > self.product_uom_qty:
                     raise UserError(_("Total Qty Import Lebih Besar dari Qty RI"))


    @api.onchange('periode')
    def onchange_periode(self):
        if self.periode:
            self.tahun = self.periode.tahun.value

    @api.one
    @api.depends('periode','ket', 'tipe', 'tipe_proses','dept','struktur_gaji')
    def _compute_nama(self):
        if self.periode and self.ket and self.tipe_proses == 'all':
           self.name = 'PAYROLL ' + str(self.tipe).upper() + ' ' + str(self.periode.name).upper() + ' ' +str(self.ket).upper()
        if self.periode and self.ket and self.tipe_proses == 'department':
           self.name = 'PAYROLL ' + str(self.tipe).upper() + ' ' + str(self.dept.name).upper() + ' ' + str(self.periode.name).upper() + ' ' +str(self.ket).upper()
        if self.periode and self.ket and self.tipe_proses == 'struktur':
           self.name = 'PAYROLL ' + str(self.tipe).upper() + ' ' + str(self.struktur_gaji.name).upper() + ' ' + str(self.periode.name).upper() + ' ' +str(self.ket).upper()

        if self.periode and not self.ket and self.tipe_proses == 'all':
           self.name = 'PAYROLL ' + str(self.tipe).upper() + ' ' + str(self.periode.name).upper()
        if self.periode and not self.ket and self.tipe_proses == 'department':
           self.name = 'PAYROLL ' + str(self.tipe).upper() + ' ' + str(self.dept.name).upper() + ' ' + str(self.periode.name).upper()
        if self.periode and not self.ket and self.tipe_proses == 'struktur':
           self.name = 'PAYROLL ' + str(self.tipe).upper() + ' ' + str(self.struktur_gaji.name).upper() + ' ' + str(self.periode.name).upper()

        if not self.periode and self.ket and self.tipe_proses == 'all':
           self.name = 'PAYROLL ' + str(self.tipe).upper() + ' ' + str(self.ket).upper()
        if not self.periode and self.ket and self.tipe_proses == 'department':
           self.name = 'PAYROLL ' + str(self.tipe).upper() + ' ' + str(self.dept.name).upper() + ' ' + str(self.ket).upper()
        if not self.periode and self.ket and self.tipe_proses == 'struktur':
           self.name = 'PAYROLL ' + str(self.tipe).upper() + ' ' + str(self.struktur_gaji.name).upper() + ' ' + str(self.ket).upper()


    @api.one
    def action_get(self):
        if self.tipe_proses == 'all':
          gaji_auto_obj = self.env['tbl_msi_payroll_line']
          if self.source == 'raw':
           cari = self.env['hr.employee'].search([('active', '=', True)])
           if cari:
              for hasil in cari:
                 if not hasil.is_exit:
                    kontrak = self.env['hr.contract'].search([('employee_id', '=', hasil.id)], order="id desc", limit=1)
                    if kontrak:
                       header_payroll = gaji_auto_obj.create({
                          'details': self.id,
                          'state': 'draft',
                          'employee': hasil.id,
                          'name': hasil.nik,
                          'contract_id': kontrak.id,
                          'gol_gaji': kontrak.gol_gaji,
                          'periode': self.periode.id,
                          'tahun': self.tahun,
                       })
              self.state = 'data'

          if self.source == 'import':

           self.env.cr.execute('select id, nik from hr_employee where active = %s and nik is not null and is_exit = %s', (True, False))
           for item2 in self.env.cr.fetchall():
                self.env.cr.execute("INSERT into tbl_msi_payroll_line (details, state, employee, periode, name, date, tahun, tipe) values (%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, 'draft', item2[0], self.periode.id, item2[1], fields.Date.today(),self.periode.tahun.value, self.tipe))

                self.env.cr.execute("UPDATE tbl_payrol_raw_import set periode = %s, employee = %s where name = %s and date >= %s and date <= %s",(self.periode.id, item2[0], item2[1], self.periode.date_awal, self.periode.date_akhir))

           self.state = 'data'
        
        if self.tipe_proses == 'department':
          if not self.dept:
            raise UserError(_("Department Belum Diisi"))
          else:
            gaji_auto_obj = self.env['tbl_msi_payroll_line']
            if self.source == 'raw':
             cari = self.env['hr.employee'].search([('active', '=', True),('department_id', '=', self.dept.id)])
             if cari:
                for hasil in cari:
                   if not hasil.is_exit:
                      kontrak = self.env['hr.contract'].search([('employee_id', '=', hasil.id)], order="id desc", limit=1)
                      if kontrak:
                         header_payroll = gaji_auto_obj.create({
                            'details': self.id,
                            'state': 'draft',
                            'employee': hasil.id,
                            'name': hasil.nik,
                            'contract_id': kontrak.id,
                            'gol_gaji': kontrak.gol_gaji,
                            'periode': self.periode.id,
                            'tahun': self.tahun,
                         })
                self.state = 'data'

            if self.source == 'import':

             self.env.cr.execute('select id, nik from hr_employee where active = %s and nik is not null and is_exit = %s and department_id = %s', (True, False, self.dept.id))
             for item2 in self.env.cr.fetchall():
                  self.env.cr.execute("INSERT into tbl_msi_payroll_line (details, state, employee, periode, name, date, tahun, tipe) values (%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, 'draft', item2[0], self.periode.id, item2[1], fields.Date.today(),self.periode.tahun.value, self.tipe))

                  self.env.cr.execute("UPDATE tbl_payrol_raw_import set periode = %s, employee = %s where name = %s and date >= %s and date <= %s",(self.periode.id, item2[0], item2[1], self.periode.date_awal, self.periode.date_akhir))

             self.state = 'data'   

        if self.tipe_proses == 'struktur':
          if not self.struktur_gaji:
            raise UserError(_("Strukture Payroll Belum Diisi"))
          else:
            gaji_auto_obj = self.env['tbl_msi_payroll_line']
            if self.source == 'raw':
             cari = self.env['hr.employee'].search([('active', '=', True)])
             if cari:
                for hasil in cari:
                   if not hasil.is_exit:
                      kontrak = self.env['hr.contract'].search([('employee_id', '=', hasil.id),('struktur_gaji', '=', self.struktur_gaji.id)], order="id desc", limit=1)
                      if kontrak:
                         header_payroll = gaji_auto_obj.create({
                            'details': self.id,
                            'state': 'draft',
                            'employee': hasil.id,
                            'name': hasil.nik,
                            'contract_id': kontrak.id,
                            'gol_gaji': kontrak.gol_gaji,
                            'periode': self.periode.id,
                            'tahun': self.tahun,
                         })
                self.state = 'data'

            if self.source == 'import':
             cari = self.env['hr.employee'].search([('active', '=', True)])
             if cari:
                for hasil in cari:
                   if not hasil.is_exit:
                      kontrak = self.env['hr.contract'].search([('employee_id', '=', hasil.id),('struktur_gaji', '=', self.struktur_gaji.id)], order="id desc", limit=1)
                      if kontrak:

                       self.env.cr.execute('select id, nik from hr_employee where id = %s', (kontrak.employee_id.id, ))
                       for item2 in self.env.cr.fetchall():
                            self.env.cr.execute("INSERT into tbl_msi_payroll_line (details, state, employee, periode, name, date, tahun, tipe) values (%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, 'draft', item2[0], self.periode.id, item2[1], fields.Date.today(),self.periode.tahun.value, self.tipe))

                            self.env.cr.execute("UPDATE tbl_payrol_raw_import set periode = %s, employee = %s where name = %s and date >= %s and date <= %s",(self.periode.id, item2[0], item2[1], self.periode.date_awal, self.periode.date_akhir))

                       self.state = 'data'

    @api.one
    def action_payroll_struktur(self):
        for emp in self.detail:
            emp.action_get()

        if self.source == 'raw':
            self.state = 'proses'

        if self.source == 'import':
          aa=0
          self.state = 'tax_send'

    @api.one
    def action_proses_payroll_line(self):
        for emp in self.detail:
            emp.action_auto()
        self.state = 'tax_send'

    @api.one
    def action_proses_tax_kirim(self):
        for emp in self.detail:
            emp.action_proses_tax_kirim()
        self.state = 'tax_receive'

    @api.one
    def action_proses_tax_terima(self):
        for emp in self.detail:
            emp.action_proses_tax_terima()
        self.state = 'submit'

    @api.one
    def action_approve(self):
        for emp in self.detail:
            emp.action_approve()
        self.state = 'approve'

    @api.one
    def action_closing(self):
        for emp in self.detail:
            emp.action_closing()
        self.state = 'close'


    @api.one
    def action_proses_ulang(self):
        for emp in self.detail:
            emp.action_ulang()
        self.env.cr.execute("DELETE from tbl_msi_payroll_line where details = %s",(self.id,))
        self.state = 'draft'


 
class tbl_msi_payroll_line(models.Model):
    _name = 'tbl_msi_payroll_line'
    _description = "Payroll Header"
    _order = 'date desc, name'


    details = fields.Many2one('tbl_msi_payroll_bulanan','Detail')
    details_print = fields.Many2one('tbl_msi_print_payroll_batch','Detail Print')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ('close', 'Closed'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    tipe = fields.Selection([
        ('regular', 'Regular'),
        ('adhoc', 'Adhoc'),
        ('exit', 'Exit'),
        ], string='Tipe', readonly=True)

    employee = fields.Many2one('hr.employee','Employee')
    name = fields.Char('NIK', related='employee.nik', store=True)
    nik = fields.Char('NIK', related='employee.nik', store=True)
    dept = fields.Many2one('hr.department', 'Department', related='employee.department_id', store=True)
    no_npwp = fields.Char('Nomor NPWP', related='employee.no_npwp', store=True)
    ptkp = fields.Many2one('tbl_employee_ptkp','PTKP', related='employee.ptkp', store=True)
    divisi = fields.Many2one('tbl_employee_divisi', 'Divisi', related='employee.divisi', store=True)
    loc = fields.Many2one('tbl_employee_lokasi', 'Lokasi', related='employee.lokasi', store=True)
    job = fields.Char('Job Title', related='employee.job_title', store=True)
    date = fields.Date('Date', default=fields.Date.today())
    user = fields.Many2one('res.users','User', track_visibility='onchange', default=lambda self: self.env.user )
    type_id = fields.Many2one('hr.contract.type', string="Employee Category", related='contract_id.type_id', store=True)
    contract_id = fields.Many2one('hr.contract', string='Current Contract', help='Latest contract of the employee')
    loc_bayar = fields.Many2one('tbl_employee_lokasi', 'Lokasi', related='employee.lokasi', store=True, readonly=False)
    gol_gaji = fields.Char('Golongan Gaji')
    periode = fields.Many2one('tbl_payroll_period','Period') 
    tahun = fields.Integer('Tahun', required=True)
    total_allow = fields.Float('Pendapatan',digits=(16, 0))
    total_ded = fields.Float('Pengurang',digits=(16, 0))
    total_net = fields.Float('Netto',digits=(16, 0))
    total_tunj_tax = fields.Float('Tunjangan Pajak',digits=(16, 0))
    total_tax = fields.Float('Potongan Pajak',digits=(16, 0))
    total_thp = fields.Float('Take Home Pay',digits=(16, 0))

    analytic_id = fields.Many2one('account.analytic.account', string='Cost Center')
    account_id = fields.Many2one('account.account', string="Expense Account")
    tax_id = fields.Many2one('account.tax', string='Tax')
    tax_siap = fields.Boolean('Tax Ready')

    detail_manual = fields.One2many('tbl_msi_payroll_line_manual','details','Detail manual')
    detail_payroll = fields.One2many('tbl_msi_payroll_line_detail','details','Detail Paroll')

    detail_overtime = fields.One2many('tbl_msi_payroll_overtime_detail','details1','Detail Overtime')
    total_lembur = fields.Float(string='Total Lembur', compute="_compute_total_lembur", store=True)

    @api.one
    @api.depends('detail_payroll')
    def _compute_allowance(self):
        if self.detail_payroll:
           for nilai in self.detail_payroll:
               if nilai.tipe == 'Allowance':
                  self.total_allow += nilai.nominal
               if nilai.tipe == 'Deduction':
                  self.total_ded += nilai.nominal

    @api.one
    @api.depends('total_allow','total_ded')
    def _compute_net(self):
        self.total_net = self.total_allow - self.total_ded

    @api.one
    @api.depends('total_net','total_tax')
    def _compute_thp(self):
        self.total_thp = self.total_net - self.total_tax

    @api.one
    def action_get(self):
        gaji_auto_obj = self.env['tbl_msi_payroll_line_detail']
        overtime_obj = self.env['tbl_msi_payroll_overtime_detail']
        if self.details.source == 'raw':
             cari = self.env['hr.contract'].search([('employee_id', '=', self.employee.id)], order="id desc", limit=1)
             if cari:
                self.contract_id = cari.id
                self.analytic_id = cari.analytic_id.id
                self.gol_gaji = cari.gol_gaji

             else:
                raise UserError(_("Kontrak utk pegawai %s tidak ada.") % (self.employee.name,))
        
             if self.details:
                self.periode = self.details.periode.id

             #if self.detail_tunjangan:
             #   self.periode = self.detail_tunjangan.periode.id

             #if self.detail_exit:
             #   self.periode = self.detail_exit.periode.id


             if cari.struktur_gaji:
                if cari.struktur_gaji.detail:
                   for gaji in cari.struktur_gaji.detail:


                       #raise UserError(_("Struktur  ,%s ,%s ,%s ,%s ,%s ,tidak ada.") % (str(gaji.name.kategori_pendapatan),str(gaji.tipe),cari.id,gaji.name.account_id.id,str(gaji.name.tipe_potongan),))


#                       data_line2 = gaji_auto_obj.create({
#                           'details': self.id,
#                           'name': str(gaji.name.name),
#                           'kode': str(gaji.kode),
#
#                           'tipe_potongan': str(gaji.name.tipe_potongan),
#                           'periode': self.periode.id,
#                           'employee': self.employee.id,
#                           'tahun': self.periode.tahun.value,
#                           'taxable': str(gaji.name.taxable),
#                           'kategori_pendapatan': str(gaji.name.kategori_pendapatan),
#
#                           'tipe': str(gaji.tipe),
#                           'contract_id': cari.id,
#                           'account_id': gaji.name.account_id.id,
#                       })
                       self.env.cr.execute("INSERT into tbl_msi_payroll_line_detail \
                          (details, name, kode, tipe_potongan, periode, employee, tahun, taxable, kategori_pendapatan, tipe, contract_id, account_id) \
                          values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)\
                          ",(self.id, str(gaji.name.name),str(gaji.kode),str(gaji.name.tipe_potongan),self.periode.id,self.employee.id,self.periode.tahun.value,str(gaji.name.taxable),str(gaji.name.kategori_pendapatan),str(gaji.tipe),cari.id,gaji.name.account_id.id))


                else:
                   raise UserError(_("Struktur  %s tidak ada.") % (self.employee.name,))
             else:
                raise UserError(_("Struktur  %s tidak ada.") % (self.employee.name,))

             self.state = 'submit'
        if self.details.source == 'import':

#           #raise UserError(_(self.name))
            self.env.cr.execute('select gapok, jabatan, tanggung_jawab, hm, retase, lembur, hadir, kinerja, transport, bersih_unit, uang_saku,\
                           makan, field, komunikasi, bonus, pab, hd, se, spkl, a_pph21, a_jk,\
                           a_jkk, a_jkm, a_jht, a_jp, a_bpjs_kesehatan,\
                           d_jht, d_jp, d_bpjs_kesehatan, d_bpjs_tenagakerja, d_pph21, d_lainnya from tbl_payrol_raw_import where employee = %s and periode = %s limit 1', (self.employee.id, self.periode.id))

            semua = self.env.cr.fetchall()

            if semua:
               for item in semua:

                if item[0] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan  from tbl_payrol_item_struktur where kode_import = %s', ('gapok',))
                   for item2 in self.env.cr.fetchall():
                       #raise UserError(_(item2[2]))
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[0], self.periode.tahun.value,item2[5],item2[6]))                       

                if item[1] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('jabatan',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[1], self.periode.tahun.value,item2[5],item2[6]))                        
 
                if item[2] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('tanggung_jawab',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[2], self.periode.tahun.value,item2[5],item2[6]))
                        
                if item[3] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('hm',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[3], self.periode.tahun.value,item2[5],item2[6]))
                        

                if item[4] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('retase',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[4], self.periode.tahun.value,item2[5],item2[6]))
                        

                if item[5] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('lembur',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[5], self.periode.tahun.value,item2[5],item2[6]))

                if item[6] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('hadir',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[6], self.periode.tahun.value,item2[5],item2[6]))
                        

                if item[7] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('kinerja',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[7], self.periode.tahun.value,item2[5],item2[6]))
                        

                if item[8] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('transport',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[8], self.periode.tahun.value,item2[5],item2[6]))
                        

                if item[9] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('bersih_unit',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[9], self.periode.tahun.value,item2[5],item2[6]))
                        

                if item[10] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('uang_saku',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[10], self.periode.tahun.value,item2[5],item2[6]))
                        

                if item[11] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('makan',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[11], self.periode.tahun.value,item2[5],item2[6]))
                        

                if item[12] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('field',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[12], self.periode.tahun.value,item2[5],item2[6]))
                        

                if item[13] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('komunikasi',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[13], self.periode.tahun.value,item2[5],item2[6]))
                        

                if item[14] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('bonus',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[14], self.periode.tahun.value,item2[5],item2[6]))
                        

                if item[15] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('pab',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[15], self.periode.tahun.value,item2[5],item2[6]))
                        

                if item[16] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('hd',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[16], self.periode.tahun.value,item2[5],item2[6]))
                        

                if item[17] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('se',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[17], self.periode.tahun.value,item2[5],item2[6]))
                        

                if item[18] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('spkl',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[18], self.periode.tahun.value,item2[5],item2[6]))
                                                                        

                if item[21] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('a_jkk',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[21], self.periode.tahun.value,item2[5],item2[6]))
                        
                if item[22] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('a_jkm',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[22], self.periode.tahun.value,item2[5],item2[6]))
                        
                if item[23] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('a_jht',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[23], self.periode.tahun.value,item2[5],item2[6]))
                        
                if item[24] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('a_jp',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[24], self.periode.tahun.value,item2[5],item2[6]))
                        
                if item[25] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('a_jk',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[25], self.periode.tahun.value,item2[5],item2[6]))
                        
                if item[26] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('d_jht',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[26], self.periode.tahun.value,item2[5],item2[6]))
                        
                if item[27] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('d_jp',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[27], self.periode.tahun.value,item2[5],item2[6]))                      
                if item[28] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('d_bpjs_kesehatan',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[28], self.periode.tahun.value,item2[5],item2[6]))
                       
                if item[29] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('d_bpjs_tenagakerja',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[29], self.periode.tahun.value,item2[5],item2[6]))                       

                if item[31] > 0:
                   self.env.cr.execute('select name, kode, tipe, account_id, tipe_potongan, taxable, kategori_pendapatan   from tbl_payrol_item_struktur where kode_import = %s', ('d_lainnya',))
                   for item2 in self.env.cr.fetchall():
                       self.env.cr.execute("insert into tbl_msi_payroll_line_detail (details, name, kode, tipe, account_id, tipe_potongan, periode, employee, nominal, tahun, taxable, kategori_pendapatan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id, item2[0], item2[1],item2[2],item2[3],item2[4],self.periode.id,self.employee.id,item[31], self.periode.tahun.value,item2[5],item2[6]))

               self.env.cr.execute("UPDATE tbl_msi_payroll_line_detail set tipe1 = %s where details = %s",(self.tipe, self.id))   
                        
      # OVERTIME
        total_lembur=0
        if self.detail_overtime:
           self.detail_overtime.unlink()

        self.env.cr.execute('Select nama_hari, sc_date_a, sc_date_in, sc_date_out, act_date_in, act_date_out, lembur_spkl_start, lembur_spkl_end, total_lembur From tbl_msi_rekap_attendance\
                             Where sc_date_a >= %s and sc_date_a <= %s and employee = %s' ,(self.periode.date_awal, self.periode.date_akhir, self.employee.id))

        for row in self.env.cr.fetchall():
            # raise UserError(_('TEST'))

#                 data_line5 = overtime_obj.create({
#                    'details1': self.id,
#                    'nama_hari': row[0],
#                    'sc_date_a': row[1],
#                    'sc_date_in': row[2],
#                    'sc_date_out': row[3],
#                    'act_date_in': row[4],
#                    'act_date_out': row[5],
#                    'lembur_spkl_start': row[6],
#                    'lembur_spkl_end': row[7],
#                    'total_lembur': row[8],
#                 })

                 self.env.cr.execute("INSERT into tbl_msi_payroll_overtime_detail \
                     (details1, nama_hari, sc_date_a, sc_date_in, sc_date_out, act_date_in, act_date_out, lembur_spkl_start, lembur_spkl_end, total_lembur) \
                     values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)\
                     ",(self.id,row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
                 
        self.env.cr.execute("select total_lembur from tbl_msi_payroll_overtime_detail where details1 = %s", (self.id,))
        for hasil in self.env.cr.fetchall():
            total_lembur +=  int(hasil[0])
        self.total_lembur = total_lembur


    @api.one
    def action_auto(self):
        if self.detail_payroll:
           cari = self.env['hr.contract'].search([('id', '=', self.contract_id.id)], order="id desc", limit=1)
           for item in  self.detail_payroll:
               if item.kode == 'AFLD':
                  if not cari.u_field_hdr:
                     item.nominal = cari.u_field    
                  else:
                     kali=0
                     self.env.cr.execute('select count(id) from tbl_payrol_raw \
                             where date >= %s and date <= %s and employee = %s and state = %s and tipe=%s', (self.periode.date_awal,self.periode.date_akhir,self.employee.id,'approve', 'attendance'))
                     for hasil in self.env.cr.fetchall():
                         kali = hasil[0]
                     item.nominal = cari.u_field * int(kali)

               if item.kode == 'GJP':
                  item.nominal = cari.wage  

               if item.kode == 'AJBT':
                  item.nominal = cari.u_jabatan 

               if item.kode == 'AAHLI':
                  item.nominal = cari.u_keahlian 

               if item.kode == 'ABERSIH':
                  item.nominal = cari.u_kebersihan  

               if item.kode == 'AKLG':
                  item.nominal = cari.u_keluarga  

               if item.kode == 'AKHS':
                  item.nominal = cari.u_khusus 

               if item.kode == 'AKMK':
                  item.nominal = cari.u_komunikasi  

               if item.kode == 'APDA':
                  item.nominal = cari.u_daerah  

               if item.kode == 'ARUMAH':
                  item.nominal = cari.u_perumahan  

               if item.kode == 'AMEDI':
                  if not cari.u_medium_hdr:
                     item.nominal = cari.u_medium   
                  else:
                     kali=0
                     self.env.cr.execute('select count(id) from tbl_payrol_raw \
                             where date >= %s and date <= %s and employee = %s and state = %s and tipe=%s', (self.periode.date_awal,self.periode.date_akhir,self.employee.id,'approve', 'attendance'))
                     for hasil in self.env.cr.fetchall():
                         kali = hasil[0]
                     item.nominal = cari.u_medium * int(kali)
                   

               if item.kode == 'AHD':
                  item.nominal = cari.u_hd

               if item.kode == 'ASE':
                  item.nominal = cari.u_se 


               if item.kode == 'ATJWB':
                  item.nominal = cari.u_tanggung_jawab 

               # if item.kode == 'AKINERJA':
               #    item.nominal = cari.u_kinerja  

               if item.kode == 'ASAKU':
                  if not cari.u_saku_hdr:
                     item.nominal = cari.u_saku  
                  else:
                     kali=0
                     self.env.cr.execute('select count(id) from tbl_payrol_raw \
                             where date >= %s and date <= %s and employee = %s and state = %s and tipe=%s', (self.periode.date_awal,self.periode.date_akhir,self.employee.id,'approve', 'attendance'))
                     for hasil in self.env.cr.fetchall():
                         kali = hasil[0]
                     item.nominal = cari.u_saku * int(kali)
                   
               if item.kode == 'TJM':
                  if not cari.u_makan_hdr:
                     item.nominal = cari.u_makan  
                  else:
                     kali=0
                     self.env.cr.execute('select count(id) from tbl_payrol_raw \
                             where date >= %s and date <= %s and employee = %s and state = %s and tipe=%s', (self.periode.date_awal,self.periode.date_akhir,self.employee.id,'approve', 'attendance'))
                     for hasil in self.env.cr.fetchall():
                         kali = hasil[0]
                     item.nominal = cari.u_makan * int(kali) 


               if item.kode == 'AUT':
                  if not cari.u_transport_hdr:
                     item.nominal = cari.u_transport  
                  else:
                     kali=0
                     self.env.cr.execute('select count(id) from tbl_payrol_raw \
                             where date >= %s and date <= %s and employee = %s and state = %s and tipe=%s', (self.periode.date_awal,self.periode.date_akhir,self.employee.id,'approve', 'attendance'))
                     for hasil in self.env.cr.fetchall():
                         kali = hasil[0]
                     item.nominal = cari.u_transport * int(kali)
  
               if item.kode == 'AHDR':
                  if not cari.u_kehadiran_hdr:
                     item.nominal = cari.u_kehadiran 
                  else:
                     kali=0
                     self.env.cr.execute('select count(id) from tbl_payrol_raw \
                             where date >= %s and date <= %s and employee = %s and state = %s and tipe=%s', (self.periode.date_awal,self.periode.date_akhir,self.employee.id,'approve', 'attendance'))
                     for hasil in self.env.cr.fetchall():
                         kali = hasil[0]
                     item.nominal = cari.u_kehadiran * int(kali)


               if item.kode == 'ALBR':
                     kali=0
                     self.env.cr.execute('select sum(nominal) from tbl_payrol_raw \
                             where date >= %s and date <= %s and employee = %s and state = %s and tipe=%s', (self.periode.date_awal,self.periode.date_akhir,self.employee.id,'approve', 'lembur'))
                     hasil1 = self.env.cr.fetchall()
                     if hasil1:
                        for hasil in hasil1:
                            kali = hasil[0]
                     else:
                         kali=0
                     item.nominal = kali

               if item.kode == 'AHM':
                     kali=0
                     self.env.cr.execute('select sum(nominal) from tbl_payrol_raw \
                             where date >= %s and date <= %s and employee = %s and state = %s and tipe=%s', (self.periode.date_awal,self.periode.date_akhir,self.employee.id,'approve', 'hour'))
                     hasil1 = self.env.cr.fetchall()
                     if hasil1:
                        for hasil in hasil1:
                            kali = hasil[0]
                     else:
                         kali=0
                     item.nominal = kali


               if item.kode == 'ARETASE':
                     kali=0
                     self.env.cr.execute('select sum(nominal) from tbl_payrol_raw \
                             where date >= %s and date <= %s and employee = %s and state = %s and tipe=%s', (self.periode.date_awal,self.periode.date_akhir,self.employee.id,'approve', 'retase'))
                     hasil1 = self.env.cr.fetchall()
                     if hasil1:
                        for hasil in hasil1:
                            kali = hasil[0]
                     else:
                         kali=0
                     item.nominal = kali

               if item.kode == 'AKINERJA':
                     kali=0
                     self.env.cr.execute('select sum(nominal) from tbl_payrol_raw \
                             where date >= %s and date <= %s and employee = %s and state = %s and tipe=%s', (self.periode.date_awal,self.periode.date_akhir,self.employee.id,'approve', 'kinerja'))
                     hasil1 = self.env.cr.fetchall()
                     if hasil1:
                        for hasil in hasil1:
                            kali = hasil[0]
                     else:
                         kali=0
                     item.nominal = kali


               if item.kode == 'DLATE':
                  if not cari.u_terlambat_hdr:
                     item.nominal = cari.u_terlambat 
                  else:
                     kali=0
                     self.env.cr.execute('select count(id) from tbl_payrol_raw \
                             where date >= %s and date <= %s and employee = %s and state = %s and late > %s and tipe=%s', (self.periode.date_awal,self.periode.date_akhir,self.employee.id,'approve',0, 'attendance'))
                     for hasil in self.env.cr.fetchall():
                         kali = hasil[0]
                     item.nominal = cari.u_terlambat * int(kali)

               if item.kode == 'DBPJSKES':
                     item.nominal = cari.wage * (cari.bpjs_kesehatan.karyawan/100)

               if item.kode == 'DJHT':
                     item.nominal = cari.wage * (cari.jht.karyawan/100)

               if item.kode == 'DJP':
                     item.nominal = cari.wage * (cari.jp.karyawan/100)


               if item.kode == 'AJHT':
                     item.nominal = cari.wage * (cari.jht.perusahaan/100)

               if item.kode == 'AJKK':
                     item.nominal = cari.wage * (cari.jkk.perusahaan/100)

               if item.kode == 'AJKM':
                     item.nominal = cari.wage * (cari.jkm.perusahaan/100)

               if item.kode == 'AJK':
                     item.nominal = cari.wage * (cari.bpjs_kesehatan.perusahaan/100)

               if item.kode == 'AJP':
                     item.nominal = cari.wage * (cari.jp.perusahaan/100)

               if item.kode == 'DBPJSNAKER':
                     item.nominal = (cari.wage * (cari.jht.perusahaan/100)) + (cari.wage * (cari.jkk.perusahaan/100)) + (cari.wage * (cari.jkm.perusahaan/100)) + (cari.wage * (cari.jp.perusahaan/100))


    @api.one
    def action_approve(self):
        for emp in self.detail_payroll:
            emp.action_approve()
        self.state = 'approve'


    @api.one
    def action_closing(self):
        for emp in self.detail_payroll:
            emp.action_closing()
        self.state = 'close'





    @api.one
    def action_proses_tax_kirim(self):
        tax_input_obj = self.env['tbl_msi_tax_input']
        total_reg=0
        total_ireg=0
        for emp in self.detail_payroll:
            #raise UserError(_(emp.tipe))
            if emp.tipe == 'Allowance' and emp.taxable and emp.kategori_pendapatan == 'REG' :
               total_reg += emp.nominal
            if emp.tipe == 'Allowance' and emp.taxable and emp.kategori_pendapatan == 'IREG' :
               total_ireg += emp.nominal
            if emp.tipe == 'Deduction':
               tax = tax_input_obj.create({
                      'details': str(emp.details.id),
                      'name': str(emp.name),
                      'kode': str(emp.kode),
                      'tipe': str(emp.tipe),
                      'nominal': emp.nominal,
                      'employee': str(emp.employee.name),
                      'nik': str(emp.employee.nik),
                      'tipe_potongan': str(emp.tipe_potongan),
                      'payroll_date': self.details.periode.date_akhir,
               })

        tax = tax_input_obj.create({
                      'details': str(self.id),
                      'name': 'Earning Reguler',
                      'kode': 'REG',
                      'tipe': 'Allowance',
                      'nominal': total_reg,
                      'employee': str(self.employee.name),
                      'nik': str(self.name),
                      'payroll_date': self.details.periode.date_akhir,
        })

        tax = tax_input_obj.create({
                      'details': str(self.id),
                      'name': 'Earning Ireguler',
                      'kode': 'IREG',
                      'tipe': 'Allowance',
                      'nominal': total_ireg,
                      'employee': str(self.employee.name),
                      'nik': str(self.name),
                      'payroll_date': self.details.periode.date_akhir,
        })



    @api.one
    def action_proses_tax_terima(self):
        self.total_allow = 0
        pay_det_obj = self.env['tbl_msi_payroll_line_detail']
        if not self.tax_siap:
           raise UserError(_("Data Tax belum ada"))
        else:
           allow_detail = 0
           deduc_detail = 0
           allow_manual = 0
           deduc_manual = 0
           for nom in self.detail_payroll:
               if nom.tipe == 'Allowance' :
                  allow_detail += nom.nominal
               if nom.tipe == 'Deduction' :
                  deduc_detail += nom.nominal
           for man in self.detail_manual:
               if man.tipe == 'Allowance' :
                  allow_manual += man.nominal
                  cari = self.env['tbl_payrol_item_struktur'].search([('kode', '=', str(man.kode))], order="id desc", limit=1)
                  if cari:
                       tax = pay_det_obj.create({
                            'details': self.id,
                            'name': cari.name,
                            'kode': cari.kode,
                            'tipe': cari.tipe,
                            'account_id': cari.account_id.id,
                            'tipe_potongan': cari.tipe_potongan,
                            'periode': self.periode.id,
                            'employee': self.employee.id,
                            'nominal': man.nominal,
                            'tahun': int(self.periode.tahun.value),
                            'taxable': cari.taxable,
                            'kategori_pendapatan': cari.kategori_pendapatan,
                       })

               if man.tipe == 'Deduction' :
                  deduc_manual += man.nominal
                  cari = self.env['tbl_payrol_item_struktur'].search([('kode', '=', str(man.kode))], order="id desc", limit=1)
                  if cari:
                       tax = pay_det_obj.create({
                            'details': self.id,
                            'name': cari.name,
                            'kode': cari.kode,
                            'tipe': cari.tipe,
                            'account_id': cari.account_id.id,
                            'tipe_potongan': cari.tipe_potongan,
                            'periode': self.periode.id,
                            'employee': self.employee.id,
                            'nominal': man.nominal,
                            'tahun': int(self.periode.tahun.value),
                            'taxable': cari.taxable,
                            'kategori_pendapatan': cari.kategori_pendapatan,
                       })


           self.total_allow = allow_detail + allow_manual
           self.total_ded = deduc_detail + deduc_manual
           self.total_thp = self.total_allow - self.total_ded - self.total_tax + self.total_tunj_tax


    @api.one
    def action_ulang(self):
        self.env.cr.execute("DELETE from tbl_msi_payroll_line_detail where details = %s",(self.id,))
        self.env.cr.execute("DELETE from tbl_msi_tax_input where details = %s",(str(self.id),)) 

    @api.multi
    def action_payslip_sent(self):
        self.ensure_one()
        template = self.env.ref('msi_hr_payroll.msi_email_template_payslip2', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        lang = self.env.context.get('lang')
        if template and template.lang:
            lang = template._render_template(template.lang, 'tbl_msi_payroll_line', self.id)
        self = self.with_context(lang=lang)
        ctx = {
            'default_model': 'tbl_msi_payroll_line',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template.id),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'model_description': "Payslip",
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    @api.one
    def action_ambil_data(self):
        overtime_obj = self.env['tbl_msi_payroll_overtime_detail']
      
        if self.detail_overtime:
           self.detail_overtime.unlink()

        self.env.cr.execute('Select nama_hari, sc_date_a, sc_date_in, sc_date_out, act_date_in, act_date_out, lembur_spkl_start, lembur_spkl_end, total_lembur From tbl_msi_rekap_attendance\
                             Where sc_date_a >= %s and sc_date_a <= %s and employee = %s' ,(self.periode.date_awal, self.periode.date_akhir, self.employee.id))

        for row in self.env.cr.fetchall():
            # raise UserError(_('TEST'))

                 data_line5 = overtime_obj.create({
                    'details1': self.id,
                    'nama_hari': row[0],
                    'sc_date_a': row[1],
                    'sc_date_in': row[2],
                    'sc_date_out': row[3],
                    'act_date_in': row[4],
                    'act_date_out': row[5],
                    'lembur_spkl_start': row[6],
                    'lembur_spkl_end': row[7],
                    'total_lembur': row[8],
                 })
        if self.detail_overtime:
          for wo in self:
            for harga in wo.detail_overtime:        
               wo.total_lembur += harga.total_lembur
    @api.one
    @api.depends('detail_overtime','detail_overtime.total_lembur')
    def _compute_total_lembur(self):
        if self.detail_overtime:
          for wo in self:
            for harga in wo.detail_overtime:        
               wo.total_lembur += harga.total_lembur

class tbl_msi_payroll_line_manual(models.Model):
    _name = 'tbl_msi_payroll_line_manual'
    _description = "Payroll Detail Manual"
    _order = 'kode, name'

    details = fields.Many2one('tbl_msi_payroll_line','Detail')
    name = fields.Many2one('tbl_payrol_item_struktur','Name')
    kode = fields.Char('Code', related='name.kode', store=True)
    tipe = fields.Selection([
        ('Deduction', 'Deduction'),
        ('Allowance', 'Allowance'),
        ], string='Tipe', default='Allowance', related='name.tipe', store=True)
    nominal = fields.Float('Nominal')


class tbl_msi_payroll_line_detail(models.Model):
    _name = 'tbl_msi_payroll_line_detail'
    _description = "Payroll Detail Line"
    _order = 'tipe, name'

    details = fields.Many2one('tbl_msi_payroll_line','Detail')
    name = fields.Char('Name')
    kode = fields.Char('Code')
    tipe = fields.Char('Type')
    nominal = fields.Float('Nominal',digits=(16, 0))
    periode = fields.Many2one('tbl_payroll_period','Period', related='details.periode', store=True)
    tahun = fields.Integer('Tahun', required=True)
    account_id = fields.Many2one('account.account', string="Expense Account", required=True, readonly=False)
    employee = fields.Many2one('hr.employee','Employee', related='details.employee', store=True)
    nik = fields.Char('NIK', related='employee.nik')
    dept = fields.Many2one('hr.department', 'Department', related='employee.department_id', store=True)
    no_npwp = fields.Char('Nomor NPWP', related='employee.no_npwp', store=True)
    ptkp = fields.Many2one('tbl_employee_ptkp','PTKP', related='employee.ptkp', store=True)
    divisi = fields.Many2one('tbl_employee_divisi', 'Divisi', related='employee.divisi', store=True)
    analytic_id = fields.Many2one('account.analytic.account', string='Cost Center', related='details.analytic_id', store=True, readonly=False)
    contract_id = fields.Many2one('hr.contract', string='Current Contract', help='Latest contract of the employee', related='details.contract_id', store=True)
    type_id = fields.Many2one('hr.contract.type', string="Employee Category", related='contract_id.type_id', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ('close', 'Closed'),
        ], string='Status', related='details.state', store=True, readonly=False)

    tipe1 = fields.Selection([
        ('regular', 'Regular'),
        ('adhoc', 'Adhoc'),
        ('exit', 'Exit'),
        ], string='Tipe', readonly=True)

    tipe_potongan = fields.Char(string='Tipe Potongan') 
    taxable = fields.Boolean('Taxable') 
    kategori_pendapatan = fields.Char('Kategori Pendapatan') 


    @api.one
    def action_approve(self):
        self.state = 'approve'


    @api.one
    def action_closing(self):
        self.state = 'close'


class tbl_msi_payroll_overtime_detail(models.Model):
    _name = 'tbl_msi_payroll_overtime_detail'
    _order = 'sc_date_a asc'


    details1 = fields.Many2one('tbl_msi_payroll_line','Detail')
    name = fields.Date('Date', readonly=True, related='details1.date')
    nama_hari = fields.Char('Nama hari', help='Nama Hari')
    sc_date_a = fields.Date('Tanggal', help='Jadual Tgl Masuk')
    sc_date_in = fields.Datetime('Jad Tgl Msk', help='Jadual Jam Masuk')
    sc_date_out = fields.Datetime('Jad Tgl Plg', help='Jadual Jam Pulang')
    act_date_in = fields.Datetime('Akt Tgl Msk', help='Aktual Jam Masuk')
    act_date_out = fields.Datetime('Akt Tgl Plg', help='Aktual Jam Pulang')
    lembur_spkl_start = fields.Datetime('Jad SPKL Msk')
    lembur_spkl_end = fields.Datetime('Jad SPKL Plg')
    total_lembur = fields.Float('Total Lembur (Jam)', help='Total Lembur dalam jam', digits=(16, 2))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ('create_bill', 'Create Bill'),
        ('done', 'Done'),
        ], string='Status', readonly=True, related='details1.state')
    user = fields.Many2one('res.users','User', readonly=True, related='details1.user')