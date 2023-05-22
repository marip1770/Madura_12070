# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError
from odoo import api, fields, models
from odoo.tools.float_utils import float_round, float_compare
# from odoo.tools.float_utils import float_compare

from datetime import date 
import math



class msi_budget_account_invoice(models.Model):
    _inherit = 'account.invoice'

    department_id = fields.Many2one('hr.department', 'Department',compute='_compute_requested_dept', store=True)
    parent_id = fields.Many2one('hr.employee', 'Manager',compute='_compute_requested_dept', store=True)

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


    def _prepare_invoice_line_from_po_line(self, line):
        if line.product_id.purchase_method == 'purchase':
            qty = line.product_qty - line.qty_invoiced
        else:
            qty = line.qty_received - line.qty_invoiced
        if float_compare(qty, 0.0, precision_rounding=line.product_uom.rounding) <= 0:
            qty = 0.0
        taxes = line.taxes_id
        invoice_line_tax_ids = line.order_id.fiscal_position_id.map_tax(taxes, line.product_id, line.order_id.partner_id)
        invoice_line = self.env['account.invoice.line']
        date = self.date or self.date_invoice
        data = {
            'purchase_line_id': line.id,
            'name': line.order_id.name + ': ' + line.name,
            'origin': line.order_id.origin,
            'uom_id': line.product_uom.id,
            'product_id': line.product_id.id,
            'account_id': invoice_line.with_context({'journal_id': self.journal_id.id, 'type': 'in_invoice'})._default_account(),
            'price_unit': line.order_id.currency_id._convert(
                line.price_unit, self.currency_id, line.company_id, date or fields.Date.today(), round=False),
            'quantity': qty,
            'discount': 0.0,
            'is_service': True,
            'account_analytic_id': line.account_analytic_id.id,
            'cost_center_id': line.cost_center_id.id,
            'analytic_tag_ids': line.analytic_tag_ids.ids,
            'invoice_line_tax_ids': invoice_line_tax_ids.ids
        }
        account = invoice_line.with_context(purchase_line_id=line.id).get_invoice_line_account('in_invoice', line.product_id, line.order_id.fiscal_position_id, self.env.user.company_id)
        if account:
            data['account_id'] = account.id
        return data


class msi_budget_account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'


    department_id = fields.Many2one('hr.department', 'Department',compute='_compute_requested_dept', store=True)

    @api.multi
    @api.depends('product_id', 'invoice_id')
    def _compute_requested_dept(self):
        for rec in self:
            rec.department_id = rec.invoice_id.department_id.id

    # @api.multi
    # @api.onchange('product_id','product_qty','department_id')
    # def onchange_product_id2(self):
    #     budget_dept_obj =self.env['tbl_msi_crossovered_budget_lines_department'].search([('name', '=', self.department_id.id)])
    #     cost_dept_obj =self.env['tbl_msi_account_cost_center_department'].search([('name', '=', self.department_id.id)])
    #     budget_dept_list = []
    #     cost_dept_list = []
    #     for data in budget_dept_obj:
    #         budget_dept_list.append(data.details.analytic_account_id.id)
    #     for data1 in cost_dept_obj:
    #         cost_dept_list.append(data1.details.id)
    #     domain = {'account_analytic_id': [('id', 'in', budget_dept_list)],'cost_center_id': [('id', 'in', cost_dept_list)]}
    #     result = {'domain': domain}
    #     return result

# class msi_budget_account_invoice_bill_line(models.Model):
#     _inherit = 'tbl_invoice_line'


#     department_id = fields.Many2one('hr.department', 'Department',compute='_compute_requested_dept', store=True)
#     cost_center_id = fields.Many2one(
#         'account.cost.center',
#         string='Cost Center',
#         index=True)

#     @api.multi
#     @api.depends('product_id', 'invoice_id')
#     def _compute_requested_dept(self):
#         for rec in self:
#             rec.department_id = rec.invoice_id.department_id.id

#     @api.multi
#     @api.onchange('product_id','product_qty','department_id')
#     def onchange_product_id2(self):
#         budget_dept_obj =self.env['tbl_msi_crossovered_budget_lines_department'].search([('name', '=', self.department_id.id)])
#         cost_dept_obj =self.env['tbl_msi_account_cost_center_department'].search([('name', '=', self.department_id.id)])
#         budget_dept_list = []
#         cost_dept_list = []
#         for data in budget_dept_obj:
#             budget_dept_list.append(data.details.analytic_account_id.id)
#         for data1 in cost_dept_obj:
#             cost_dept_list.append(data1.details.id)
#         domain = {'account_analytic_id': [('id', 'in', budget_dept_list)],'cost_center_id': [('id', 'in', cost_dept_list)]}
#         result = {'domain': domain}
#         return result
