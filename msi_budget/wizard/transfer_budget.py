# Copyright 2018-2019 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).


from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from datetime import datetime


class tbl_msi_transfer_budget(models.TransientModel):
    _name = "tbl_msi_transfer_budget"
    _description = "Budget Transfer"

    @api.model
    def _default_budget(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', [])
        data = self.env['crossovered.budget'].browse(active_ids)
        return data.id

    budget_id = fields.Many2one('crossovered.budget', string='Budget', default=_default_budget)
    asal_budget_id = fields.Many2one('crossovered.budget.lines', string='Asal Budget')
    tujuan_budget_id = fields.Many2one('crossovered.budget.lines', string='Tujuan Budget')
    nominal = fields.Float(string='Noimal')

