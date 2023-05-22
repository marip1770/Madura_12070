from odoo import api, fields, models, _

class purchase_request(models.Model):

    _inherit = "purchase.request"

    lokasi = fields.Many2one('stock.location','Lokasi')

    @api.onchange('mpr_requested_by')
    def onchange_employee_location(self):
        self.lokasi = self.mpr_requested_by.lokasi_gudang.lot_stock_id.id

    
    def action_print(self):
        return self.env.ref('bisa_purchase_request.action_report_purchase_request').report_action(self)
    
    

class purchase_request_line(models.Model):

    _inherit="purchase.request.line"

    lokasi = fields.Many2one('stock.location','Lokasi' , related='request_id.lokasi',store=True)
    on_hand_qty = fields.Float('Quantity on Hand', compute='_compute_on_hand_qty')

    @api.depends('product_id',
                 'lokasi')
    def _compute_on_hand_qty(self):
        for request in self:
            if request.product_id and request.lokasi:
              request.env.cr.execute("select sum(quantity) from stock_quant where product_id = %s and location_id = %s", (request.product_id.id, request.lokasi.id))
              for req in request.env.cr.fetchall():
                on_hand = req[0]
                request.on_hand_qty = on_hand


