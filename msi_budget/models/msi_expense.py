# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError
from odoo import api, fields, models
from odoo.tools.float_utils import float_round

from datetime import date 
import math



class msi_budget_expense_sheet(models.Model):
    _inherit = 'hr.expense.sheet'

    department_id = fields.Many2one('hr.department', 'Department',compute='_compute_employee_id',store=True)
    group_head_id = fields.Many2one('hr.department', 'Group Head',compute='_compute_department_id',store=True)
    # parent_id = fields.Many2one('hr.employee', 'Manager')

    @api.onchange('employee_id')
    def onchange_user_id(self):
        if self.employee_id:
                self.department_id = self.employee_id.department_id.id

    @api.multi
    @api.depends('employee_id')
    def _compute_employee_id(self):
        if self.employee_id:
                self.department_id = self.employee_id.department_id.id

    @api.multi
    @api.depends('department_id')
    def _compute_department_id(self):
        if self.department_id:
            gh = self.env['hr.department'].search([('parent_id', '=', self.department_id.id)])
            if gh:
                self.group_head_id = self.department_id.id
            else:
                self.group_head_id = self.department_id.parent_id.id


class msi_budget_expense(models.Model):
    _inherit = 'hr.expense'


    department_id = fields.Many2one('hr.department', 'Department',compute='_compute_employee_id',store=True)
    group_head_id = fields.Many2one('hr.department', 'Group Head',compute='_compute_department_id',store=True)
    # parent_id = fields.Many2one('hr.employee', 'Manager')
    cost_center_id = fields.Many2one(
        'account.cost.center',
        string='Cost Center',
        index=True)
    amount_budget = fields.Monetary(
        string='Amount Budget', currency_field='currency_id', default=0.0,compute='_compute_amount_budget',store=True)

    @api.multi
    @api.depends('analytic_account_id', 'date')
    def _compute_amount_budget(self):
        for rec in self:
            if rec.analytic_account_id and rec.date:
                nilai1 = 0
                budget = rec.env['crossovered.budget.lines'].search([('analytic_account_id', '=', rec.analytic_account_id.id),('date_from', '<=', rec.date),('date_to', '>=', rec.date)])
                if budget :
                    for line in budget:
                        nilai = 0
                        nilai = line.planned_amount - line.practical_amount
                        nilai1 += nilai
                    rec.amount_budget = nilai1

    @api.onchange('employee_id')
    def onchange_user_id(self):
        if self.employee_id:
                self.department_id = self.employee_id.department_id.id

    @api.onchange('amount_budget','total_amount')
    def onchange_amount_budget(self):
        if self.analytic_account_id and self.product_id:
            if self.total_amount > self.amount_budget:
                raise UserError("Total Melebihi Budget")

    @api.one
    @api.depends('employee_id')
    def _compute_employee_id(self):
        if self.employee_id:
                self.department_id = self.employee_id.department_id.id

    @api.one
    @api.depends('department_id')
    def _compute_department_id(self):
        if self.department_id:
            gh = self.env['hr.department'].search([('parent_id', '=', self.department_id.id)])
            if gh:
                self.group_head_id = self.department_id.id
            else:
                self.group_head_id = self.department_id.parent_id.id


    # @api.multi
    # @api.onchange('product_id','product_qty','department_id')
    # def onchange_product_id2(self):
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
    #     domain = {'analytic_account_id': ['|',('id', 'in', budget_dept_list),('id', 'in', budget_gh_list)],'cost_center_id': ['|',('id', 'in', cost_dept_list),('id', 'in', cost_gh_list)]}
    #     result = {'domain': domain}
    #     return result


    # @api.multi
    # @api.onchange('product_id','analytic_account_id')
    # def onchange_analytic_account_id2(self):
    #     if self.product_id and self.analytic_account_id:
    #       if self.product_id.property_account_expense_id:
    #         # raise UserError("aaa")
    #         budget_obj =self.env['crossovered.budget.lines'].search([('analytic_account_id', '=', self.analytic_account_id.id)])

    #         account_list = []
    #         for budget in budget_obj:
    #             account_list.append(budget.general_budget_id.account_ids.id)
    #         # raise UserError(_('%s' % (account_list, )))
    #         account_obj =self.env['account.account'].search([('id', 'in', account_list),('id', '=', self.product_id.property_account_expense_id.id)])
    #         # raise UserError(_('%s' % (account_obj, )))
    #         # for acc in account_obj:
    #         if not account_obj:
    #                 raise UserError("Account tidak sesuai dengan di budget")
    #       else:
    #         if self.product_id.categ_id.property_account_expense_categ_id:
    #           budget_obj =self.env['crossovered.budget.lines'].search([('analytic_account_id', '=', self.analytic_account_id.id)])
    #           account_list = []
    #           for budget in budget_obj:
    #               account_list.append(budget.general_budget_id.account_ids.id)
    #         # raise UserError(_('%s' % (account_list, )))
    #           account_obj =self.env['account.account'].search([('id', 'in', account_list),('id', '=', self.product_id.categ_id.property_account_expense_categ_id.id)])
    #         # for acc in account_obj:
    #           if not account_obj:
    #                   raise UserError("Account tidak sesuai dengan di budget")
    #         else:
    #           raise UserError("Account pada Product Belum di Setting")

