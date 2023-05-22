# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError
from odoo import api, fields, models
import datetime
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.addons import decimal_precision as dp


_STATES = [
    ('draft', 'Draft'),
    ('to_approve', 'To be approved'),
    ('appr1', 'Approve1'),
    ('appr2', 'Approve2'),
    ('appr3', 'Approve3'),
    ('appr4', 'Approve4'),
    ('appr5', 'Approve5'),
    ('appr6', 'Approve6'),
    ('appr7', 'Approve7'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('done', 'Done')
]


class tbl_msi_approval(models.Model):
    _name = 'tbl_msi_approval'

    tingkat_approval_so = fields.Selection([
         ('0','0'),
         ('1','1'),
         ('2','2'),
    ], string='Tingkat Approval SO', default='0', store=True)
    grup_approve_so1 = fields.Many2one('res.groups','Grup Approve 1')
    grup_approve_so2 = fields.Many2one('res.groups','Grup Approve 2')

    tingkat_approval_pr = fields.Selection([
         ('0','0'),
         ('1','1'),
         ('2','2'),
         ('3','3'),
         ('4','4'),
         ('5','5'),
         ('6','6'),
         ('7','7'),
    ], string='Tingkat Approval PR', default='0', store=True)
    grup_approve_pr1 = fields.Many2one('res.groups','Grup Approve 1')
    grup_approve_pr2 = fields.Many2one('res.groups','Grup Approve 2')
    grup_approve_pr3 = fields.Many2one('res.groups','Grup Approve 3')
    grup_approve_pr4 = fields.Many2one('res.groups','Grup Approve 4')
    grup_approve_pr5 = fields.Many2one('res.groups','Grup Approve 5')
    grup_approve_pr6 = fields.Many2one('res.groups','Grup Approve 6')
    grup_approve_pr7 = fields.Many2one('res.groups','Grup Approve 7')
    nominal_approve_pr0 = fields.Float('Nominal Approve 0',size=19,digits=(19, 0))
    # nominal_approve_pr01 = fields.Float('Nominal Approve 0',size=19,digits=(19, 0))
    nominal_approve_pr1 = fields.Float('Nominal Approve 1',size=19,digits=(19, 0))
    nominal_approve_pr2 = fields.Float('Nominal Approve 2',size=19,digits=(19, 0))
    nominal_approve_pr3 = fields.Float('Nominal Approve 3',size=19,digits=(19, 0))
    nominal_approve_pr4 = fields.Float('Nominal Approve 4',size=19,digits=(19, 0))
    nominal_approve_pr5 = fields.Float('Nominal Approve 5',size=19,digits=(19, 0))
    nominal_approve_pr6 = fields.Float('Nominal Approve 6',size=19,digits=(19, 0))
    nominal_approve_pr7 = fields.Float('Nominal Approve 7',size=19,digits=(19, 0))

    tingkat_approval_po = fields.Selection([
         ('0','0'),
         ('1','1'),
         ('2','2'),
         ('3','3'),
         ('4','4'),
         ('5','5'),
         ('6','6'),
         ('7','7'),
    ], string='Tingkat Approval PO', default='0', store=True)
    grup_approve_po1 = fields.Many2one('res.groups','Grup Approve 1')
    grup_approve_po2 = fields.Many2one('res.groups','Grup Approve 2')
    grup_approve_po3 = fields.Many2one('res.groups','Grup Approve 3')
    grup_approve_po4 = fields.Many2one('res.groups','Grup Approve 4')
    grup_approve_po5 = fields.Many2one('res.groups','Grup Approve 5')
    grup_approve_po6 = fields.Many2one('res.groups','Grup Approve 6')
    grup_approve_po7 = fields.Many2one('res.groups','Grup Approve 7')
    nominal_approve_po0 = fields.Float('Nominal Approve 0',size=19,digits=(19, 0))
    nominal_approve_po1 = fields.Float('Nominal Approve 1',size=19,digits=(19, 0))
    nominal_approve_po2 = fields.Float('Nominal Approve 2',size=19,digits=(19, 0))
    nominal_approve_po3 = fields.Float('Nominal Approve 3',size=19,digits=(19, 0))
    nominal_approve_po4 = fields.Float('Nominal Approve 4',size=19,digits=(19, 0))
    nominal_approve_po5 = fields.Float('Nominal Approve 5',size=19,digits=(19, 0))
    nominal_approve_po6 = fields.Float('Nominal Approve 6',size=19,digits=(19, 0))
    nominal_approve_po7 = fields.Float('Nominal Approve 7',size=19,digits=(19, 0))

    tingkat_approval_payment = fields.Selection([
         ('0','0'),
         ('1','1'),
         ('2','2'),
         ('3','3'),
         ('4','4'),
         ('5','5'),
    ], string='Tingkat Approval Payment', default='0', store=True)
    grup_approve_payment1 = fields.Many2one('res.groups','Grup Approve 1')
    grup_approve_payment2 = fields.Many2one('res.groups','Grup Approve 2')
    grup_approve_payment3 = fields.Many2one('res.groups','Grup Approve 3')
    grup_approve_payment4 = fields.Many2one('res.groups','Grup Approve 4')
    grup_approve_payment5 = fields.Many2one('res.groups','Grup Approve 5')
    nominal_approve_payment0 = fields.Float('Nominal Approve 0',size=19,digits=(19, 0))
    nominal_approve_payment1 = fields.Float('Nominal Approve 1',size=19,digits=(19, 0))
    nominal_approve_payment2 = fields.Float('Nominal Approve 2',size=19,digits=(19, 0))
    nominal_approve_payment3 = fields.Float('Nominal Approve 3',size=19,digits=(19, 0))
    nominal_approve_payment4 = fields.Float('Nominal Approve 4',size=19,digits=(19, 0))
    nominal_approve_payment5 = fields.Float('Nominal Approve 5',size=19,digits=(19, 0))

    tingkat_approval_advance = fields.Selection([
         ('0','0'),
         ('1','1'),
         ('2','2'),
         ('3','3'),
    ], string='Tingkat Approval Advance ', default='0', store=True)
    grup_approve_advance1 = fields.Many2one('res.groups','Grup Advance 1')
    grup_approve_advance2 = fields.Many2one('res.groups','Grup Advance 2')
    grup_approve_advance3 = fields.Many2one('res.groups','Grup Advance 3')
    nominal_approve_advance0 = fields.Float('Nominal Advance 0',size=19,digits=(19, 0))
    nominal_approve_advance1 = fields.Float('Nominal Advance 1',size=19,digits=(19, 0))
    nominal_approve_advance2 = fields.Float('Nominal Advance 2',size=19,digits=(19, 0))
    nominal_approve_advance3 = fields.Float('Nominal Advance 3',size=19,digits=(19, 0))


class tbl_msi_approval_so(models.Model):
    _inherit = "sale.order"

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('appr1', 'Approve1'),
        ('appr2', 'Approve2'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3, default='draft')

    @api.multi
    def action_confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
        if cari:
           if cari.tingkat_approval_so == '0':
              self.write({
                 'state': 'sale',
                 'confirmation_date': fields.Datetime.now()
              })
              self._action_confirm()
              if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
                 self.action_done()
              kontrak_obj = self.env['tbl_bisa_contract_management']
              detail_kontrak_obj = self.env['tbl_bisa_detail_contract']
              projek_obj = self.env['project.project']
      
              if self.order_line:
                #   create_projek = projek_obj.create({
                #       'name': self.env['ir.sequence'].next_by_code('seq_projek'),
                #   })
      
                  data_kontrak = kontrak_obj.create({
                      'name': self.id,
                      'nama_customer': self.partner_id.id,
                  })
                  for dc in self.order_line:
                      if dc.product_id.servis == 'hauling':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'hauling',
                              'detailcontrak': data_kontrak.id,
                          })
      
                      if dc.product_id.servis == 'hrm':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'hrm',
                              'detailcontrak': data_kontrak.id,
                          })
      
                      if dc.product_id.servis == 'rental':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'portal',
                              'detailcontrak': data_kontrak.id,
                          })
      
                      if dc.product_id.servis == 'port':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'port',
                              'detailcontrak': data_kontrak.id,
                          })
      
                      if dc.product_id.servis == 'fuel_truck':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'fuel_truck',
                              'detailcontrak': data_kontrak.id,
                          })
      
                      if dc.product_id.servis == 'water_truck':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'water_truck',
                              'detailcontrak': data_kontrak.id,
                          })

                      if dc.product_id.servis == 'tls':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'tls',
                              'detailcontrak': data_kontrak.id,
                          })
              
           else:
              self.write({
                 'state': 'appr1',
              })
        return True

    def act_appr1(self):
      cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
      if cari:
         if cari.tingkat_approval_so == '1':
              self.write({
                 'state': 'sale',
                 'confirmation_date': fields.Datetime.now()
              })
              self._action_confirm()
              if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
                 self.action_done()
              kontrak_obj = self.env['tbl_bisa_contract_management']
              detail_kontrak_obj = self.env['tbl_bisa_detail_contract']
              projek_obj = self.env['project.project']
      
              if self.order_line:
                #   create_projek = projek_obj.create({
                #       'name': self.env['ir.sequence'].next_by_code('seq_projek'),
                #   })
      
                  data_kontrak = kontrak_obj.create({
                      'name': self.id,
                      'nama_customer': self.partner_id.id,
                  })
                  for dc in self.order_line:
                      if dc.product_id.servis == 'hauling':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'hauling',
                              'detailcontrak': data_kontrak.id,
                          })
      
                      if dc.product_id.servis == 'hrm':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'hrm',
                              'detailcontrak': data_kontrak.id,
                          })
      
                      if dc.product_id.servis == 'rental':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'portal',
                              'detailcontrak': data_kontrak.id,
                          })
      
                      if dc.product_id.servis == 'port':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'port',
                              'detailcontrak': data_kontrak.id,
                          })
      
                      if dc.product_id.servis == 'fuel_truck':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'fuel_truck',
                              'detailcontrak': data_kontrak.id,
                          })
      
                      if dc.product_id.servis == 'water_truck':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'water_truck',
                              'detailcontrak': data_kontrak.id,
                          })

                      if dc.product_id.servis == 'tls':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'tls',
                              'detailcontrak': data_kontrak.id,
                          })
              return True
         else:
            self.state = 'appr2'

    def act_appr2(self):
      cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
      if cari:
         if cari.tingkat_approval_so == '2':
              self.write({
                 'state': 'sale',
                 'confirmation_date': fields.Datetime.now()
              })
              self._action_confirm()
              if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
                 self.action_done()
              kontrak_obj = self.env['tbl_bisa_contract_management']
              detail_kontrak_obj = self.env['tbl_bisa_detail_contract']
              projek_obj = self.env['project.project']
      
              if self.order_line:
                #   create_projek = projek_obj.create({
                #       'name': self.env['ir.sequence'].next_by_code('seq_projek'),
                #   })
      
                  data_kontrak = kontrak_obj.create({
                      'name': self.id,
                      'nama_customer': self.partner_id.id,
                  })
                  for dc in self.order_line:
                      if dc.product_id.servis == 'hauling':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'hauling',
                              'detailcontrak': data_kontrak.id,
                          })
      
                      if dc.product_id.servis == 'hrm':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'hrm',
                              'detailcontrak': data_kontrak.id,
                          })
      
                      if dc.product_id.servis == 'rental':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'portal',
                              'detailcontrak': data_kontrak.id,
                          })
      
                      if dc.product_id.servis == 'port':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'port',
                              'detailcontrak': data_kontrak.id,
                          })
      
                      if dc.product_id.servis == 'fuel_truck':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'fuel_truck',
                              'detailcontrak': data_kontrak.id,
                          })
      
                      if dc.product_id.servis == 'water_truck':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'water_truck',
                              'detailcontrak': data_kontrak.id,
                          })

                      if dc.product_id.servis == 'tls':
                          data_detail_kontrak = detail_kontrak_obj.create({
                            #   'nama_projek': create_projek.id,
                              'produk': dc.product_id.id,
                              'quantity': dc.product_uom_qty,
                              'uom': dc.product_uom.id,
                              'harga': dc.price_unit,
                              'total': dc.price_subtotal,
                              'tipe': 'tls',
                              'detailcontrak': data_kontrak.id,
                          })
              return True
         else:
              self.write({
                 'state': 'sale',
                 'confirmation_date': fields.Datetime.now()
              })
              self._action_confirm()
              if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
                 self.action_done()

    @api.multi
    def action_confirm_ori(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
        if cari:
           if cari.tingkat_approval_so == '0':
              self.write({
                 'state': 'sale',
                 'confirmation_date': fields.Datetime.now()
              })
              self._action_confirm()
              if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
                 self.action_done()
           else:
              self.write({
                 'state': 'appr1',
              })

        return True


class tbl_msi_approval_pr(models.Model):
    _inherit = 'purchase.request'

    @api.multi
    @api.depends('state')
    def _compute_is_editable(self):
        for rec in self:
            if rec.state in ('to_approve', 'appr1', 'appr2', 'appr3', 'appr4', 'appr5', 'appr6', 'appr7', 'approved', 'rejected', 'done'):
                rec.is_editable = False
            else:
                rec.is_editable = True


    state = fields.Selection(selection=_STATES,
                             string='Status',
                             index=True,
                             track_visibility='onchange',
                             required=True,
                             copy=False,
                             default='draft')

    total_estimate = fields.Float(
        string='Total Estimate',
        compute='_compute_estimate',
        readonly=True)

    @api.depends('line_ids')
    def _compute_estimate(self):
        self.total_estimate = sum(self.mapped(
            'line_ids.estimated_cost'))




    @api.multi
    def button_approved(self):
        cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
        if cari:
           if cari.tingkat_approval_pr == '0':
              if not self.total_estimate > cari.nominal_approve_pr0:
                 self.write({
                     'state': 'approved',
                 })
              else:
                self.write({
                   'state': 'appr1',
                })

           else:
              self.write({
                 'state': 'appr1',
              })

    def act_appr1(self):
        cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
        if cari:
           if cari.tingkat_approval_pr == '1':
              if self.total_estimate < cari.nominal_approve_pr1:
                 self.write({
                     'state': 'approved',
                 })
              else:
                self.write({
                   'state': 'appr2',
                })

           else:
              if cari.tingkat_approval_pr == '0':
                 self.write({
                    'state': 'approved',
                 })
              else:
                 #raise UserError(_(self.total_estimate))
                 if  self.total_estimate < cari.nominal_approve_pr1:
                    self.write({
                       'state': 'approved',
                    })
                 else:
                    self.write({
                       'state': 'appr2',
                    })


    def act_appr2(self):
        cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
        if cari:
           if cari.tingkat_approval_pr == '2':
              if self.total_estimate < cari.nominal_approve_pr2:
                 self.write({
                     'state': 'approved',
                 })
              else:
                self.write({
                   'state': 'appr3',
                })

           else:
              if cari.tingkat_approval_pr == '1':
                 self.write({
                    'state': 'approved',
                 })
              else:
                 if self.total_estimate < cari.nominal_approve_pr2:
                    self.write({
                       'state': 'approved',
                    })
                 else:
                    self.write({
                       'state': 'appr3',
                    })


    def act_appr3(self):
        cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
        if cari:
           if cari.tingkat_approval_pr == '3':
              if self.total_estimate < cari.nominal_approve_pr3:
                 self.write({
                     'state': 'approved',
                 })
              else:
                self.write({
                   'state': 'appr4',
                })

           else:
              if cari.tingkat_approval_pr == '2':
                 self.write({
                    'state': 'approved',
                 })
              else:
                 if self.total_estimate < cari.nominal_approve_pr3:
                    self.write({
                       'state': 'approved',
                    })
                 else:
                    self.write({
                       'state': 'appr4',
                    })

    def act_appr4(self):
        cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
        if cari:
           if cari.tingkat_approval_pr == '4':
              if self.total_estimate < cari.nominal_approve_pr4:
                 self.write({
                     'state': 'approved',
                 })
              else:
                self.write({
                   'state': 'appr5',
                })

           else:
              if cari.tingkat_approval_pr == '3':
                 self.write({
                    'state': 'approved',
                 })
              else:
                 if self.total_estimate < cari.nominal_approve_pr4:
                    self.write({
                       'state': 'approved',
                    })
                 else:
                    self.write({
                       'state': 'appr5',
                    })

    def act_appr5(self):
        cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
        if cari:
           if cari.tingkat_approval_pr == '5':
              if self.total_estimate < cari.nominal_approve_pr5:
                 self.write({
                     'state': 'approved',
                 })
              else:
                self.write({
                   'state': 'appr6',
                })

           else:
              if cari.tingkat_approval_pr == '4':
                 self.write({
                    'state': 'approved',
                 })
              else:
                 if self.total_estimate < cari.nominal_approve_pr5:
                    self.write({
                       'state': 'approved',
                    })
                 else:
                    self.write({
                       'state': 'appr6',
                    })

    def act_appr6(self):
        cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
        if cari:
           if cari.tingkat_approval_pr == '6':
              if self.total_estimate < cari.nominal_approve_pr6:
                 self.write({
                     'state': 'approved',
                 })
              else:
                self.write({
                   'state': 'appr7',
                })

           else:
              if cari.tingkat_approval_pr == '5':
                 self.write({
                    'state': 'approved',
                 })
              else:
                 if self.total_estimate < cari.nominal_approve_pr6:
                    self.write({
                       'state': 'approved',
                    })
                 else:
                    self.write({
                       'state': 'appr7',
                    })

    def act_appr7(self):
        cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
        if cari:
           if cari.tingkat_approval_pr == '7':
              if self.total_estimate < cari.nominal_approve_pr7:
                 self.write({
                     'state': 'approved',
                 })
              else:
                self.write({
                   'state': 'approved',
                })

           else:
              if cari.tingkat_approval_pr == '6':
                 self.write({
                    'state': 'approved',
                 })
              else:
                 #raise UserError(_(self.total_estimate))
                 if  self.total_estimate < cari.nominal_approve_pr7:
                    self.write({
                       'state': 'approved',
                    })
                 else:
                    self.write({
                       'state': 'approved',
                    })

    def act_cancel(self):
          self.write({
                       'state': 'draft',
          })

class tbl_msi_approval_o(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('appr1', 'Approve1'),
        ('appr2', 'Approve2'),
        ('appr3', 'Approve3'),
        ('appr4', 'Approve4'),
        ('appr5', 'Approve5'),
        ('appr6', 'Approve6'),
        ('appr7', 'Approve7'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')



    @api.multi
    def button_confirm(self):
        for order in self:

           cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
           if cari:
              if cari.tingkat_approval_po == '0':
                 if order.amount_total < cari.nominal_approve_pr0:
                    # if order.state not in ['draft', 'sent']:
                    #      continue
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                    else:
                       order.write({'state': 'purchase'})
              else:
                order.write({
                   'state': 'appr1',
                })

           else:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step'\
                    or (order.company_id.po_double_validation == 'two_step'\
                        and order.amount_total < self.env.user.company_id.currency_id._convert(
                            order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})


    def act_appr1(self):
        for order in self:
         cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
         if cari:
           if cari.tingkat_approval_po == '1':
              if order.amount_total < cari.nominal_approve_po1:
                    # if order.state not in ['draft', 'sent']:
                    #      continue
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                    else:
                       order.write({'state': 'purchase'})
              else:
                order.write({
                   'state': 'appr2',
                })

           else:
              if cari.tingkat_approval_po == '0':
                 order.write({
                    'state': 'purchase',
                 })
              if cari.tingkat_approval_po == '2':
                if order.amount_total < cari.nominal_approve_po1:
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                    else:
                       order.write({'state': 'purchase'})
                else:
                  order.write({
                   'state': 'appr2',
                  })
              else:
                if order.amount_total < cari.nominal_approve_po1:
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                    else:
                       order.write({'state': 'purchase'})
                else:
                  order.write({
                   'state': 'appr2',
                  })
         else:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step'\
                    or (order.company_id.po_double_validation == 'two_step'\
                        and order.amount_total < self.env.user.company_id.currency_id._convert(
                            order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})

    def act_appr2(self):
        for order in self:
         cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
         if cari:
           if cari.tingkat_approval_po == '2':
              if order.amount_total < cari.nominal_approve_po2:
                    # raise UserError(_("cc"))
                    # if order.state not in ['draft', 'sent']:
                    #      raise UserError(_("11"))
                    #      continue
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                       # raise UserError(_("aa"))
                    else:
                       # raise UserError(_("bb"))
                       order.write({'state': 'purchase'})
              else:
                order.write({
                   'state': 'appr3',
                })

           else:
              if cari.tingkat_approval_po == '1':
                 order.write({
                    'state': 'purchase',
                 })
              if cari.tingkat_approval_po == '3':
                if order.amount_total < cari.nominal_approve_po2:
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                    else:
                       order.write({'state': 'purchase'})
                else:
                  order.write({
                   'state': 'appr3',
                  })
              else:
                if order.amount_total < cari.nominal_approve_po2:
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                    else:
                       order.write({'state': 'purchase'})
                else:
                  order.write({
                   'state': 'appr3',
                  })

    def act_appr3(self):
        for order in self:
         cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
         if cari:
           if cari.tingkat_approval_po == '3':
              if order.amount_total < cari.nominal_approve_po3:
                    # raise UserError(_("cc"))
                    # if order.state not in ['draft', 'sent']:
                    #      raise UserError(_("11"))
                    #      continue
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                       # raise UserError(_("aa"))
                    else:
                       # raise UserError(_("bb"))
                       order.write({'state': 'purchase'})
              else:
                order.write({
                   'state': 'appr4',
                })

           else:
              if cari.tingkat_approval_po == '2':
                 order.write({
                    'state': 'purchase',
                 })
              if cari.tingkat_approval_po == '4':
                if order.amount_total < cari.nominal_approve_po3:
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                    else:
                       order.write({'state': 'purchase'})
                else:
                  order.write({
                   'state': 'appr4',
                  })
              else:
                if order.amount_total < cari.nominal_approve_po3:
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                    else:
                       order.write({'state': 'purchase'})
                else:
                  order.write({
                   'state': 'appr4',
                  })


    def act_appr4(self):
        for order in self:
         cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
         if cari:
           if cari.tingkat_approval_po == '4':
              if order.amount_total < cari.nominal_approve_po4:
                    # raise UserError(_("cc"))
                    # if order.state not in ['draft', 'sent']:
                    #      raise UserError(_("11"))
                    #      continue
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                       # raise UserError(_("aa"))
                    else:
                       # raise UserError(_("bb"))
                       order.write({'state': 'purchase'})
              else:
                order.write({
                   'state': 'appr5',
                })

           else:
              if cari.tingkat_approval_po == '3':
                 order.write({
                    'state': 'purchase',
                 })
              if cari.tingkat_approval_po == '5':
                if order.amount_total < cari.nominal_approve_po4:
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                    else:
                       order.write({'state': 'purchase'})
                else:
                  order.write({
                   'state': 'appr5',
                  })
              else:
                if order.amount_total < cari.nominal_approve_po4:
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                    else:
                       order.write({'state': 'purchase'})
                else:
                  order.write({
                   'state': 'appr5',
                  })


    def act_appr5(self):
        for order in self:
         cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
         if cari:
           if cari.tingkat_approval_po == '5':
              if order.amount_total < cari.nominal_approve_po5:
                    # raise UserError(_("cc"))
                    # if order.state not in ['draft', 'sent']:
                    #      raise UserError(_("11"))
                    #      continue
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                       # raise UserError(_("aa"))
                    else:
                       # raise UserError(_("bb"))
                       order.write({'state': 'purchase'})
              else:
                order.write({
                   'state': 'appr6',
                })

           else:
              if cari.tingkat_approval_po == '4':
                 order.write({
                    'state': 'purchase',
                 })
              if cari.tingkat_approval_po == '6':
                if order.amount_total < cari.nominal_approve_po5:
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                    else:
                       order.write({'state': 'purchase'})
                else:
                  order.write({
                   'state': 'appr6',
                  })
              else:
                if order.amount_total < cari.nominal_approve_po5:
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                    else:
                       order.write({'state': 'purchase'})
                else:
                  order.write({
                   'state': 'appr6',
                  })
    def act_appr6(self):
        for order in self:
         cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
         if cari:
           if cari.tingkat_approval_po == '6':
              if order.amount_total < cari.nominal_approve_po6:
                    # raise UserError(_("cc"))
                    # if order.state not in ['draft', 'sent']:
                    #      raise UserError(_("11"))
                    #      continue
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                       # raise UserError(_("aa"))
                    else:
                       # raise UserError(_("bb"))
                       order.write({'state': 'purchase'})
              else:
                order.write({
                   'state': 'appr7',
                })

           else:
              if cari.tingkat_approval_po == '5':
                 order.write({
                    'state': 'purchase',
                 })
              if cari.tingkat_approval_po == '7':
                if order.amount_total < cari.nominal_approve_po6:
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                    else:
                       order.write({'state': 'purchase'})
                else:
                  order.write({
                   'state': 'appr7',
                  })
              else:
                if order.amount_total < cari.nominal_approve_po6:
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                    else:
                       order.write({'state': 'purchase'})
                else:
                  order.write({
                   'state': 'appr7',
                  })

    def act_appr7(self):
        for order in self:
         # cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
         # if cari:
         #   if cari.tingkat_approval_po == '7':
         #      if order.amount_total < cari.nominal_approve_po7:
                    # if order.state not in ['draft', 'sent']:
                    #      continue
                    order._add_supplier_to_product()
                    
                    # Deal with double validation process
                    if order.company_id.po_double_validation == 'one_step'\
                          or (order.company_id.po_double_validation == 'two_step'\
                              and order.amount_total < self.env.user.company_id.currency_id._convert(
                                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                                 or order.user_has_groups('purchase.group_purchase_manager'):
                       order.button_approve()
                    else:
                       order.write({'state': 'purchase'})
           #    else:
           #      self.write({
           #         'state': 'purchase',
           #      })

           # else:
           #    self.write({
           #       'state': 'purchase',
           #    })

class tbl_msi_approval_payment(models.Model):
    _inherit = 'account.payment'

    state = fields.Selection([('draft', 'Draft'), ('appr1', 'Approve1'),('appr2', 'Approve2'),('appr3', 'Approve3'),('appr4', 'Approve4'),('appr5', 'Approve5'),('posted', 'Posted'), ('sent', 'Sent'), ('reconciled', 'Reconciled'), ('cancelled', 'Cancelled')], readonly=True, default='draft', copy=False, string="Status", track_visibility='onchange')


    @api.multi
    def post(self):
       cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
       if cari.tingkat_approval_payment == '0':
        if self.amount < cari.nominal_approve_payment0: 
          for rec in self:

            if rec.state != 'draft':
                raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True
        else:
              self.write({
                 'state': 'appr1',
              })

       else:
        if self.amount < cari.nominal_approve_payment0: 
          for rec in self:

            if rec.state != 'draft':
                raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True
        else:
              self.write({
                 'state': 'appr1',
              })


    @api.multi
    def act_appr1(self):
       cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
       if cari.tingkat_approval_payment == '1':
        if self.amount < cari.nominal_approve_payment1: 
          for rec in self:

            # if rec.state != 'draft':
            #     raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True
        else:
              self.write({
                 'state': 'appr2',
              })

       else:
        if cari.tingkat_approval_payment == '0':
          for rec in self:

            # if rec.state != 'draft':
            #     raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True
        else:
         if self.amount < cari.nominal_approve_payment1: 
          for rec in self:

            # if rec.state != 'draft':
            #     raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True
         else:
              self.write({
                 'state': 'appr2',
              })

    @api.multi
    def act_appr2(self):
       cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
       if cari.tingkat_approval_payment == '2':
        if self.amount < cari.nominal_approve_payment2: 
          for rec in self:

            # if rec.state != 'draft':
            #     raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True
        else:
              self.write({
                 'state': 'appr3',
              })

       else:
        if cari.tingkat_approval_payment == '1':
          for rec in self:

            # if rec.state != 'draft':
            #     raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True
        else:
         if self.amount < cari.nominal_approve_payment2: 
          for rec in self:

            # if rec.state != 'draft':
            #     raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True
         else:
              self.write({
                 'state': 'appr3',
              })

 
    @api.multi
    def act_appr3(self):
       cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
       if cari.tingkat_approval_payment == '3':
        if self.amount < cari.nominal_approve_payment3: 
          for rec in self:

            # if rec.state != 'draft':
            #     raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True
        else:
              self.write({
                 'state': 'appr4',
              })

       else:
        if cari.tingkat_approval_payment == '2':
          for rec in self:

            # if rec.state != 'draft':
            #     raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True
        else:
         if self.amount < cari.nominal_approve_payment3: 
          for rec in self:

            # if rec.state != 'draft':
            #     raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True
         else:
              self.write({
                 'state': 'appr4',
              })


 
    @api.multi
    def act_appr4(self):
       cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
       if cari.tingkat_approval_payment == '4':
        if self.amount < cari.nominal_approve_payment4: 
          for rec in self:

            # if rec.state != 'draft':
            #     raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True
        else:
              self.write({
                 'state': 'appr5',
              })

       else:
        if cari.tingkat_approval_payment == '3':
          for rec in self:

            # if rec.state != 'draft':
            #     raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True
        else:
         if self.amount < cari.nominal_approve_payment4: 
          for rec in self:

            # if rec.state != 'draft':
            #     raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True
         else:
              self.write({
                 'state': 'appr5',
              })


    @api.multi
    def act_appr5(self):
       cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
       if cari.tingkat_approval_payment == '5':
        if self.amount < cari.nominal_approve_payment5: 
          for rec in self:

            # if rec.state != 'draft':
            #     raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True
        else:
          for rec in self:

            # if rec.state != 'draft':
            #     raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True
       else:
        if cari.tingkat_approval_payment == '4':
          for rec in self:

            # if rec.state != 'draft':
            #     raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True
        else:
         if self.amount < cari.nominal_approve_payment5: 
          for rec in self:

            # if rec.state != 'draft':
            #     raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True
         else:
          for rec in self:

            # if rec.state != 'draft':
            #     raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
          return True



# class tbl_msi_acc_settlement_app(models.Model):
#     _inherit = 'tbl_msi_acc_settlement'

#     state = fields.Selection([
#         ('draft', 'Draft'),
#         ('appr', 'Approve Advanced'),
#         ('apprapp1', 'Approve1'),
#         ('apprapp2', 'Approve2'),
#         ('apprapp3', 'Approve3'),
#         ('submit2', 'Submit Settlement'),
#         ('appr2', 'Approve Settlement'),
#         ('done', 'Done'),
#         ('cancel', 'Cancelled'),
#         ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

#     data_line2 = fields.Integer('Data Line2')

#     def action_approve1(self):

#       account_move_obj = self.env['account.move']
#       account_move_line_obj = self.env['account.move.line']


#       if not self.property_account_uang_muka:
#          raise UserError(_('Account Advanced belum di set'))


#       if not self.journal_id:
#          raise UserError(_('Advanced Journal belum di set'))


#       detail_obj = self.env['account.payment']
#       data_line2 = detail_obj.create({
#             'payment_type': 'outbound',
#             'partner_type': 'supplier',
#             'partner_id': self.employee_id.address_home_id.id,
#             'amount': self.saldo,
#             'journal_id': self.journal_id.id,
#             'payment_method_id': 2,
#             'communication': 'Advanced # ' + str(self.name) + ' ' +str(self.employee_id.name),
#             'x_studio_field_cqQTC': 'Advanced # ' + str(self.name) + ' ' +str(self.employee_id.name),
#             'is_advance': True,
#             'adv_account_id': self.property_account_uang_muka.id,
#         })

#       self.state = 'apprapp1'
#       self.data_line2 = data_line2.id




#     def act_apprapp1(self):
#         for order in self:
#          cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
#          if cari:
#            if cari.tingkat_approval_advance == '1':
#               if self.saldo < cari.nominal_approve_advance1:
#                   self.payment_out_id = self.data_line2
#                   self.state = 'submit2'
#               else:
#                 self.write({
#                    'state': 'apprapp2',
#                 })

#            else:
#               if cari.tingkat_approval_advance == '0':
#                   self.payment_out_id = self.data_line2
#                   self.state = 'submit2'
#               else:
#                 if self.saldo < cari.nominal_approve_advance1:
#                   self.payment_out_id = self.data_line2
#                   self.state = 'submit2'
#                 else:
#                   self.write({
#                    'state': 'apprapp2',
#                   })
#               # else:
#               #    self.write({
#               #       'state': 'apprapp2',
#               #    })


#     def act_apprapp2(self):
#         for order in self:
#          cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
#          if cari:
#            if cari.tingkat_approval_advance == '2':
#               if self.saldo < cari.nominal_approve_advance2:
#                   self.payment_out_id = self.data_line2
#                   self.state = 'submit2'
#               else:
#                 self.write({
#                    'state': 'apprapp3',
#                 })

#            else:
#               if cari.tingkat_approval_advance == '1':
#                   self.payment_out_id = self.data_line2
#                   self.state = 'submit2'
#               else:
#                 if self.saldo < cari.nominal_approve_advance2:
#                   self.payment_out_id = self.data_line2
#                   self.state = 'submit2'
#                 else:
#                   self.write({
#                    'state': 'apprapp3',
#                   })
#               # else:
#               #    self.write({
#               #       'state': 'apprapp3',
#               #    })

#     def act_apprapp3(self):
#         for order in self:
#          cari = self.env['tbl_msi_approval'].search([('id', '>', 0)], limit=1)
#          if cari:
#            if cari.tingkat_approval_advance == '3':
#               if self.saldo < cari.nominal_approve_advance3:
#                  self.payment_out_id = self.data_line2
#                  self.state = 'submit2'
#               else:
#                  self.payment_out_id = self.data_line2
#                  self.state = 'submit2'
#            else:
#                  self.payment_out_id = self.data_line2
#                  self.state = 'submit2'


