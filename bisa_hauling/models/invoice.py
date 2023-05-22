# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError
from odoo import api, fields, models
from odoo.tools.float_utils import float_round, float_compare
# from odoo.tools.float_utils import float_compare

from datetime import date 
import math



class msi_hauling_account_invoice(models.Model):
    _inherit = 'account.invoice'

    create_billing_id = fields.Many2one('tbl_pembuatan_billing', 'Create Billing')



class msi_hauling_account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'


    harga = fields.Float('Base Rate')
    rf = fields.Float('RF')
    distance = fields.Float('Distance')