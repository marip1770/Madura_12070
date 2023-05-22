from lxml import etree
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import email_re, email_split, email_escape_char, float_is_zero, float_compare, \
    pycompat, date_utils
from odoo.exceptions import UserError, AccessError
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp

import math


class AccountAssetCategory(models.Model):
    _inherit = "account.asset.category"

    aset_kategori = fields.Many2one('tbl_bisa_aset_kategori', string='Aset Kategory')

    @api.onchange('aset_kategori')
    def onchange_aset_kategori(self):
        if self.aset_kategori:
           self.method_number = self.aset_kategori.method_number
           self.method_period = self.aset_kategori.method_period

class tbl_bisa_aset_kategori(models.Model):
    _name = 'tbl_bisa_aset_kategori'

    name = fields.Char(required=True, string="Kategori Aset")
    method_number = fields.Integer(string='Number of Entries', default=5, help="The number of depreciations needed to depreciate your asset")
    method_period = fields.Integer(string='One Entry Every (Months)', default=1, help="State here the time between 2 depreciations, in months", required=True)
