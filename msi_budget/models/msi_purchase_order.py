# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError
from odoo import api, fields, models
from odoo.tools.float_utils import float_round

from datetime import date 
import math



class msi_budget_purchase_order(models.Model):
    _inherit = 'purchase.order'

    department_id = fields.Many2one('hr.department', 'Department',compute='_compute_requested_dept', store=True)
    parent_id = fields.Many2one('hr.employee', 'Manager',compute='_compute_requested_dept', store=True)
    group_head_id = fields.Many2one('hr.department', 'Requested Group Head',compute='_compute_requested_dept',store=True)

    @api.onchange('user_id')
    def onchange_user_id(self):
        if self.user_id:
           hr_obj = self.env['hr.employee']
           dept = hr_obj.search([('user_id', '=', self.user_id.id)], limit=1, order='id desc')
           if dept:
                self.department_id = dept.department_id.id
                self.parent_id = dept.parent_id.id
           else :
                self.department_id = self.user_id.employee_id.department_id.id
                self.parent_id = self.user_id.employee_id.parent_id.id

    @api.onchange('department_id')
    def onchange_department_id(self):
        if self.department_id:
           hr_obj = self.env['hr.department']
           dept = hr_obj.search([('id', '=', self.department_id.id)], limit=1, order='id desc')
           if dept:
                if dept.manager_id:
                    self.parent_id = dept.manager_id.id

    @api.one
    @api.depends('user_id', 'department_id')
    def _compute_requested_dept(self):
        if self.user_id:
           hr_obj = self.env['hr.employee']
           dept = hr_obj.search([('user_id', '=', self.user_id.id)], limit=1, order='id desc')
           if dept:
                self.department_id = dept.department_id.id
                self.parent_id = dept.parent_id.id
           else :
                self.department_id = self.user_id.employee_id.department_id.id
                self.parent_id = self.user_id.employee_id.parent_id.id
        if self.department_id:
            hr_obj = self.env['hr.department']
            dept = hr_obj.search([('id', '=', self.department_id.id)], limit=1, order='id desc')
            if dept:
                if dept.manager_id:
                    self.parent_id = dept.manager_id.id
            gh = self.env['hr.department'].search([('parent_id', '=', self.department_id.id)])
            if gh:
                self.group_head_id = self.department_id.id
            else:
                self.group_head_id = self.department_id.parent_id.id

class msi_budget_purchase_order_line(models.Model):
    _inherit = 'purchase.order.line'

    selisih_qty = fields.Float('Selisih QTY',compute='_compute_selisih_qty', store=True)
    department_id = fields.Many2one('hr.department', 'Department',compute='_compute_requested_dept', store=True)
    group_head_id = fields.Many2one('hr.department', 'Requested Group Head',compute='_compute_department_id',store=True)
    cost_center_id = fields.Many2one(
        'account.cost.center',
        string='Cost Center',
        index=True)

    @api.multi
    @api.depends('product_qty', 'qty_received')
    def _compute_selisih_qty(self):
        for rec in self:
            rec.selisih_qty = rec.product_qty - rec.qty_received

    @api.multi
    @api.depends('product_id', 'order_id')
    def _compute_requested_dept(self):
        for rec in self:
            rec.department_id = rec.order_id.department_id.id

    @api.multi
    @api.depends('product_id', 'order_id')
    def _compute_department_id(self):
        for rec in self:
            rec.group_head_id = rec.order_id.department_id.parent_id.id

    # @api.multi
    # @api.onchange('product_id','product_qty','department_id')
    # def onchange_product_id2(self):
    #     # budget_dept_obj =self.env['tbl_msi_crossovered_budget_lines_department'].search([('name', '=', self.department_id.id)])
    #     # cost_dept_obj =self.env['tbl_msi_account_cost_center_department'].search([('name', '=', self.department_id.id)])
    #     # budget_dept_list = []
    #     # cost_dept_list = []
    #     # for data in budget_dept_obj:
    #     #     budget_dept_list.append(data.details.analytic_account_id.id)
    #     # for data1 in cost_dept_obj:
    #     #     cost_dept_list.append(data1.details.id)
    #     # domain = {'account_analytic_id': [('id', 'in', budget_dept_list)],'cost_center_id': [('id', 'in', cost_dept_list)]}
    #     # result = {'domain': domain}
    #     # return result
    #     budget_dept_obj =self.env['tbl_msi_crossovered_budget_lines_department'].search([('name', '=', self.department_id.id)])
    #     cost_dept_obj =self.env['tbl_msi_account_cost_center_department'].search([('name', '=', self.department_id.id)])
    #     budget_gh_obj =self.env['crossovered.budget.lines'].search([('group_head_id', '=', self.group_head_id.id)])
    #     cost_gh_obj =self.env['account.cost.center'].search([('group_head_id', '=', self.group_head_id.id)])
    #     budget_dept_list = []
    #     cost_dept_list = []
    #     budget_gh_list = []
    #     cost_gh_list = []
    #     for data in budget_dept_obj:
    #         budget_dept_list.append(data.details.analytic_account_id.id)
    #     for data1 in cost_dept_obj:
    #         cost_dept_list.append(data1.details.id)
    #     for data2 in budget_gh_obj:
    #         budget_gh_list.append(data2.analytic_account_id.id)
    #     for data3 in cost_gh_obj:
    #         cost_gh_list.append(data3.id)
    #     domain = {'account_analytic_id': ['|',('id', 'in', budget_dept_list),('id', 'in', budget_gh_list)],'cost_center_id': ['|',('id', 'in', cost_dept_list),('id', 'in', cost_gh_list)]}
    #     result = {'domain': domain}
    #     return result
