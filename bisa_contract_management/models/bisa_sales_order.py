# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare

class TblSaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'sale',
            'confirmation_date': fields.Datetime.now()
        })

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._action_confirm()
        if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
            self.action_done()
        kontrak_obj = self.env['tbl_bisa_contract_management']
        detail_kontrak_obj = self.env['tbl_bisa_detail_contract']
        projek_obj = self.env['project.project']

        if self.order_line:
            create_projek = projek_obj.create({
                'name': self.name,
            })

            data_kontrak = kontrak_obj.create({
                'name': self.id,
                'nama_customer': self.partner_id.id,
            })
            for dc in self.order_line:
                if dc.product_id.servis == 'hauling':
                    data_detail_kontrak = detail_kontrak_obj.create({
                        'no_projek': create_projek.id,
                        'produk': dc.product_id.id,
                        'quantity': dc.product_uom_qty,
                        'uom': dc.product_uom.id,
                        'harga': dc.price_unit,
                        'total': dc.price_subtotal,
                        'tipe': 'hauling',
                        'detailcontrak': data_kontrak.id,
                    })
                    dc.is_confirm = True

                if dc.product_id.servis == 'hrm':
                    data_detail_kontrak = detail_kontrak_obj.create({
                        'produk': dc.product_id.id,
                        'quantity': dc.product_uom_qty,
                        'uom': dc.product_uom.id,
                        'harga': dc.price_unit,
                        'total': dc.price_subtotal,
                        'tipe': 'hrm',
                        'detailcontrak': data_kontrak.id,
                    })
                    dc.is_confirm = True

                if dc.product_id.servis == 'rental':
                    data_detail_kontrak = detail_kontrak_obj.create({
                        'produk': dc.product_id.id,
                        'quantity': dc.product_uom_qty,
                        'uom': dc.product_uom.id,
                        'harga': dc.price_unit,
                        'total': dc.price_subtotal,
                        'tipe': 'portal',
                        'detailcontrak': data_kontrak.id,
                    })
                    dc.is_confirm = True

                if dc.product_id.servis == 'port':
                    data_detail_kontrak = detail_kontrak_obj.create({
                        'produk': dc.product_id.id,
                        'quantity': dc.product_uom_qty,
                        'uom': dc.product_uom.id,
                        'harga': dc.price_unit,
                        'total': dc.price_subtotal,
                        'tipe': 'port',
                        'detailcontrak': data_kontrak.id,
                    })
                    dc.is_confirm = True

                if dc.product_id.servis == 'fuel_truck':
                    data_detail_kontrak = detail_kontrak_obj.create({
                        'produk': dc.product_id.id,
                        'quantity': dc.product_uom_qty,
                        'uom': dc.product_uom.id,
                        'harga': dc.price_unit,
                        'total': dc.price_subtotal,
                        'tipe': 'fuel_truck',
                        'detailcontrak': data_kontrak.id,
                    })
                    dc.is_confirm = True

                if dc.product_id.servis == 'water_truck':
                    data_detail_kontrak = detail_kontrak_obj.create({
                        'produk': dc.product_id.id,
                        'quantity': dc.product_uom_qty,
                        'uom': dc.product_uom.id,
                        'harga': dc.price_unit,
                        'total': dc.price_subtotal,
                        'tipe': 'water_truck',
                        'detailcontrak': data_kontrak.id,
                    })
                    dc.is_confirm = True
        return True