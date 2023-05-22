# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError
from odoo import api, fields, models

import math

# class CrossoveredBudget(models.Model):
#     _inherit = "crossovered.budget"

#     @api.multi
#     def action_budget_transfer(self):
#           compose_form = self.env.ref('msi_budget.view_tbl_msi_transger_budget_wizard_form', False)
#           return {
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'res_model': 'tbl_msi_transfer_budget',
#             'views': [(compose_form.id, 'form')],
#             'view_id': compose_form.id,
#             'target': 'new',
#             # 'context': ctx,
#           }

class msi_crossovered_budget_lines(models.Model):
    _inherit = 'crossovered.budget.lines'

    avail_amount = fields.Monetary(string='Avail Amount',compute='_compute_avail_amount', group_operator=True)
    department_ids = fields.One2many('tbl_msi_crossovered_budget_lines_department', 'details', 'Department')
    group_head_id = fields.Many2one('hr.department', 'Group Head')
    transfer_in = fields.Monetary(string='Transfer In', readonly=True, default=0)
    transfer_out = fields.Monetary(string='Transfer Out', readonly=True, default=0)
    original_amount = fields.Monetary(string='Original', readonly=True, default=0)
    # theoritical_amount = fields.Monetary(
    #     compute='_compute_theoritical_amount', string='Theoretical Amount',
    #     help="Amount you are supposed to have earned/spent at this date.",store=True)

    @api.multi
    @api.depends('planned_amount','practical_amount')
    def _compute_avail_amount(self):
        for rec in self:
            rec.avail_amount = rec.planned_amount + rec.practical_amount

    # @api.multi
    # def _compute_practical_amount(self):
    #     for line in self:
    #         practical = 0
    #         budget_po = 0
    #         po_budget = self.env['purchase.order.line'].search([('account_analytic_id', '=', line.analytic_account_id.id),('selisih_qty', '<', 1),('state', 'in', ('purchase','done')),('date_planned', '>=', line.date_from),('date_planned', '<=', line.date_to)])
    #         if po_budget:
    #             budget_po = 0
    #             for po in po_budget:
    #                 budget_po += po.price_subtotal
    #         else:
    #             budget_po = 0
    #         practical = budget_po
    #         # raise UserError(_(practical))
    #         line.practical_amount = practical * -1
class msi_crossovered_budget_lines_department(models.Model):
    _name = 'tbl_msi_crossovered_budget_lines_department'

    name = fields.Many2one('hr.department', 'Department')
    details = fields.Many2one('crossovered.budget.lines', 'Budget Line')

class tbl_msi_transfer_budget(models.Model):
    _name = 'tbl_msi_transfer_budget'

    name = fields.Many2one('res.users', 'User Request', default=lambda self: self.env.user)
    user_approve = fields.Many2one('res.users', 'User Approve', readonly=True)
    budget = fields.Many2one('crossovered.budget', 'Budget', required=True)
    tanggal = fields.Date('Tanggal')
    state = fields.Selection([
         ('draft','Draft'),
         ('submit','Submit'),
         ('done','Done'),
         ('cancel','Canceled')
    ], string='State', default='draft', readonly=True)
    details = fields.One2many('tbl_msi_transfer_budget_detail', 'details', 'Detail')

    def action_submit(self):
        if self.details:
            for transfer in self.details:
                if transfer.nilai_transer > transfer.nilai_availabel:
                    raise UserError(_("Transfer dari %s ke %s tidak bisa di lakukan \n Nilai yang Ditransfer melebihi Nilai Available") % (transfer.name.name, transfer.budget_tujuan.name))

        self.state = 'submit'

    def action_approve(self):
        if self.details:
            for transfer in self.details:
                if transfer.nilai_transer > transfer.nilai_availabel:
                    raise UserError(_("Transfer dari %s ke %s tidak bisa di lakukan \n Nilai yang Ditransfer melebihi Nilai Available") % (transfer.name.name, transfer.budget_tujuan.name))
                else:
                    cari_asal = self.env['crossovered.budget.lines'].search([('analytic_account_id', '=', transfer.name.id),('crossovered_budget_id', '=', self.budget.id)], order="id desc", limit=1)
                    cari_tujuan = self.env['crossovered.budget.lines'].search([('analytic_account_id', '=', transfer.budget_tujuan.id),('crossovered_budget_id', '=', self.budget.id)], order="id desc", limit=1)
                    if cari_asal:
                        cari_asal.transfer_out += transfer.nilai_transer
                        if cari_asal.original_amount == 0:
                            cari_asal.original_amount = cari_asal.planned_amount
                            cari_asal.planned_amount -= transfer.nilai_transer
                        else:
                            cari_asal.planned_amount -= transfer.nilai_transer
                    if cari_tujuan:
                        cari_tujuan.transfer_in += transfer.nilai_transer
                        if cari_tujuan.original_amount == 0:
                            cari_tujuan.original_amount = cari_tujuan.planned_amount
                            cari_tujuan.planned_amount += transfer.nilai_transer
                        else:
                            cari_tujuan.planned_amount += transfer.nilai_transer
        self.user_approve = self.env.user
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

class tbl_msi_transfer_budget_detail(models.Model):
    _name = 'tbl_msi_transfer_budget_detail'

    details = fields.Many2one('tbl_msi_transfer_budget', 'Transfer')
    name = fields.Many2one('account.analytic.account', 'Budget Code')
    nilai_availabel = fields.Float('Nilai Available',compute='_compute_nilai_availabel')
    budget_tujuan = fields.Many2one('account.analytic.account', 'Budget Code Tujuan')
    nilai_transer = fields.Float('Nilai yang Ditransfer')
    keterangan = fields.Char('Keterangan')

    @api.multi
    @api.depends('name','details.budget')
    def _compute_nilai_availabel(self):
        for transfer in self:
            cari_asal = self.env['crossovered.budget.lines'].search([('analytic_account_id', '=', transfer.name.id),('crossovered_budget_id', '=', transfer.details.budget.id)], order="id desc", limit=1)
            if cari_asal:
                transfer.nilai_availabel = cari_asal.avail_amount