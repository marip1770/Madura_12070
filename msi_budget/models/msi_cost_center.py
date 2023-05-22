# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError
from odoo import api, fields, models

import math


class msi_account_cost_center(models.Model):
    _inherit = 'account.cost.center'

    # avail_amount = fields.Monetary(string='Avail Amount',compute='_compute_avail_amount',store=True)
    department_ids = fields.One2many('tbl_msi_account_cost_center_department', 'details', 'Department')
    group_head_id = fields.Many2one('hr.department', 'Group Head')




class msi_account_cost_center_lines_department(models.Model):
    _name = 'tbl_msi_account_cost_center_department'

    name = fields.Many2one('hr.department', 'Department')
    details = fields.Many2one('account.cost.center', 'Budget Line')