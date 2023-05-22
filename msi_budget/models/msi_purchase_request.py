# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError
from odoo import api, fields, models
from odoo.tools.float_utils import float_round
from datetime import datetime

from datetime import date 
import math



class msi_budget_purchase_request(models.Model):
    _inherit = 'purchase.request'

    mpr_requested_by = fields.Many2one('hr.employee','Requested By')
    update = fields.Char('UPDAT')
    parent_id = fields.Many2one('hr.employee', 'Manager',compute='_compute_requested_dept', store=True)
    requested_dept = fields.Many2one('hr.department', 'Requested Dept',compute='_compute_requested_dept', store=True)
    group_head_id = fields.Many2one('hr.department', 'Requested Group Head',compute='_compute_department_id',store=True)

    @api.onchange('requested_by')
    def onchange_requested_by(self):
        if self.requested_by:
           hr_obj = self.env['hr.employee']
           dept = hr_obj.search([('user_id', '=', self.requested_by.id)], limit=1, order='id desc')
           if dept:
                self.requested_dept = dept.department_id.id
                self.parent_id = dept.parent_id.id
           else :
                self.requested_dept = self.requested_by.employee_id.department_id.id
                self.assigned_to = self.requested_by.employee_id.parent_id.user_id.id
                self.parent_id = self.requested_by.employee_id.parent_id.id

    @api.onchange('requested_dept')
    def onchange_requested_dept(self):
        if self.requested_dept:
           hr_obj = self.env['hr.department']
           dept = hr_obj.search([('id', '=', self.requested_dept.id)], limit=1, order='id desc')
           if dept:
                if dept.manager_id:
                    self.assigned_to = dept.manager_id.user_id.id
                    self.parent_id = dept.manager_id.id

    @api.onchange('mpr_requested_by')
    def onchange_mpr_requested_by(self):
        if self.mpr_requested_by:
            self.requested_by = self.mpr_requested_by.user_id.id

    @api.onchange('requested_by','update')
    def onchange_request_by(self):
        if self.requested_by:
            self.mpr_requested_by = self.requested_by.employee_id.id

    @api.onchange('parent_id')
    def onchange_parent_id(self):
        if self.parent_id:
            self.assigned_to = self.parent_id.user_id.id
        else:
            self.assigned_to = ''

    @api.one
    @api.depends('requested_by', 'requested_dept')
    def _compute_requested_dept(self):
        if self.requested_by:
           hr_obj = self.env['hr.employee']
           dept = hr_obj.search([('user_id', '=', self.requested_by.id)], limit=1, order='id desc')
           if dept:
                self.requested_dept = dept.department_id.id
                self.parent_id = dept.parent_id.id
           else :
                self.requested_dept = self.requested_by.employee_id.department_id.id
                self.assigned_to = self.requested_by.employee_id.parent_id.user_id.id
                self.parent_id = self.requested_by.employee_id.parent_id.id
        if self.requested_dept:
           hr_obj = self.env['hr.department']
           dept = hr_obj.search([('id', '=', self.requested_dept.id)], limit=1, order='id desc')
           if dept:
                if dept.manager_id:
                    self.assigned_to = dept.manager_id.user_id.id
                    self.parent_id = dept.manager_id.id

    @api.one
    @api.depends('requested_dept')
    def _compute_department_id(self):
        if self.requested_dept:
            gh = self.env['hr.department'].search([('parent_id', '=', self.requested_dept.id)])
            if gh:
                self.group_head_id = self.requested_dept.id
            else:
                self.group_head_id = self.requested_dept.parent_id.id

class msi_budget_purchase_request_line(models.Model):
    _inherit = 'purchase.request.line'


    requested_dept = fields.Many2one('hr.department', 'Requested Dept',compute='_compute_requested_dept', store=True)
    group_head_id = fields.Many2one('hr.department', 'Requested Group Head',compute='_compute_department_id',store=True)
    cost_center_id = fields.Many2one(
        'account.cost.center',
        string='Cost Center',
        index=True)

    @api.multi
    @api.depends('product_id', 'request_id')
    def _compute_requested_dept(self):
        for rec in self:
            rec.requested_dept = rec.request_id.requested_dept.id

    @api.multi
    @api.depends('product_id', 'request_id','requested_dept')
    def _compute_department_id(self):
        for rec in self:
            rec.group_head_id = rec.request_id.requested_dept.parent_id.id

    @api.multi
    @api.onchange('product_id','product_qty','requested_dept','estimated_cost')
    def onchange_product_id2(self):
        budget_dept_obj =self.env['tbl_msi_crossovered_budget_lines_department'].search([('name', '=', self.requested_dept.id)])
        cost_dept_obj =self.env['tbl_msi_account_cost_center_department'].search([('name', '=', self.requested_dept.id)])
        budget_gh_obj =self.env['crossovered.budget.lines'].search([('group_head_id', '=', self.group_head_id.id)])
        cost_gh_obj =self.env['account.cost.center'].search([('group_head_id', '=', self.group_head_id.id)])
        budget_dept_list = []
        cost_dept_list = []
        budget_gh_list = []
        cost_gh_list = []
        for data in budget_dept_obj:
            budget_dept_list.append(data.details.analytic_account_id.id)
        for data1 in cost_dept_obj:
            cost_dept_list.append(data1.details.id)
        for data2 in budget_gh_obj:
            budget_gh_list.append(data2.analytic_account_id.id)
        for data3 in cost_gh_obj:
            cost_gh_list.append(data3.id)
        domain = {'analytic_account_id': ['|',('id', 'in', budget_dept_list),('id', 'in', budget_gh_list)],'cost_center_id': ['|',('id', 'in', cost_dept_list),('id', 'in', cost_gh_list)]}
        result = {'domain': domain}
        return result

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

    # @api.multi
    # def action_analytic_account_id2(self):

class PurchaseRequestLineMakePurchaseOrder(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order"

    @api.model
    def _prepare_purchase_order_line(self, po, item):
        if not item.product_id:
            raise UserError("Please select a product for all lines")
        product = item.product_id

        # Keep the standard product UOM for purchase order so we should
        # convert the product quantity to this UOM
        qty = item.product_uom_id._compute_quantity(
            item.product_qty, product.uom_po_id or product.uom_id)
        # Suggest the supplier min qty as it's done in Odoo core
        min_qty = item.line_id._get_supplier_min_qty(product, po.partner_id)
        qty = max(qty, min_qty)
        date_required = item.line_id.date_required
        vals = {
            'name': product.name,
            'order_id': po.id,
            'product_id': product.id,
            'product_uom': product.uom_po_id.id,
            'price_unit': 0.0,
            'product_qty': qty,
            'account_analytic_id': item.line_id.analytic_account_id.id,
            'cost_center_id': item.line_id.cost_center_id.id,
            'purchase_request_lines': [(4, item.line_id.id)],
            'date_planned': datetime(date_required.year, date_required.month,
                                     date_required.day),
            'move_dest_ids': [(4, x.id) for x in item.line_id.move_dest_ids]
        }
        self._execute_purchase_line_onchange(vals)
        return vals