# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import email_re, email_split, email_escape_char, float_is_zero, float_compare, \
    pycompat, date_utils
from odoo.exceptions import UserError, AccessError
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp

import math

MAP_INVOICE_TYPE_PARTNER_TYPE = {
    'out_invoice': 'customer',
    'out_refund': 'customer',
    'in_invoice': 'supplier',
    'in_refund': 'supplier',
}

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    invoice_line__bill_ids = fields.One2many('tbl_invoice_line', 'invoice_id', string='Invoice Lines bill',
        copy=True)
    # amount_by_group_bill = fields.Binary(string="Tax amount by group", compute='_amount_by_group', help="type: [(name, amount, base, formated amount, formated base)]")
    amount_untaxed_bill = fields.Monetary(string='Untaxed Amount',
        store=True, readonly=True, compute='_compute_amount_bill', track_visibility='always')
    # amount_untaxed_signed_bill = fields.Monetary(string='Untaxed Amount in Company Currency', currency_field='company_currency_id',
    #     store=True, readonly=True, compute='_compute_amount')
    # amount_untaxed_invoice_signed_bill = fields.Monetary(string='Untaxed Amount in Invoice Currency', currency_field='currency_id',
    #     readonly=True, compute='_compute_sign_taxes')
    amount_tax_bill = fields.Monetary(string='Tax',
        store=True, readonly=True, compute='_compute_amount_bill')
    # amount_tax_signed_bill = fields.Monetary(string='Tax in Invoice Currency', currency_field='currency_id',
    #     readonly=True, compute='_compute_sign_taxes')
    amount_total_bill = fields.Monetary(string='Total',
        store=True, readonly=True, compute='_compute_amount_bill')
    amount_total_selisih = fields.Monetary(string='Total Selisih',store=True, readonly=True, compute='_compute_selisih')
    avail_po_value = fields.Float(string='Avail PO Value',store=True, readonly=True, compute='_compute_origin')

    code_transaksi = fields.Char('Code Transaksi',default='New', readonly=True)
    state = fields.Selection([
            ('draft','Draft'),
            ('approve','Approve'),
            ('open', 'Open'),
            ('in_payment', 'In Payment'),
            ('paid', 'Paid'),
            ('cancel', 'Cancelled'),
        ], string='Status', index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
        help=" * The 'Draft' status is used when a user is encoding a new and unconfirmed Invoice.\n"
             " * The 'Open' status is used when user creates invoice, an invoice number is generated. It stays in the open status till the user pays the invoice.\n"
             " * The 'In Payment' status is used when payments have been registered for the entirety of the invoice in a journal configured to post entries at bank reconciliation only, and some of them haven't been reconciled with a bank statement line yet.\n"
             " * The 'Paid' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled.\n"
             " * The 'Cancelled' status is used when user cancel invoice.")
    journal_service = fields.Many2one('account.move','Journal Service',store=True, readonly=True, compute='_compute_origin')
    # amount_total_signed_bill = fields.Monetary(string='Total in Invoice Currency', currency_field='currency_id',
    #     store=True, readonly=True, compute='_compute_amount',
    #     help="Total amount in the currency of the invoice, negative for credit notes.")
    # amount_total_company_signed_bill = fields.Monetary(string='Total in Company Currency', currency_field='company_currency_id',
    #     store=True, readonly=True, compute='_compute_amount',
    #     help="Total amount in the currency of the company, negative for credit notes.")

    @api.model
    def create(self, vals):
        if not vals.get('journal_id') and vals.get('type'):
            vals['journal_id'] = self.with_context(type=vals.get('type'))._default_journal().id

        if vals.get('code_transaksi', _('New')) == _('New'):
                vals['code_transaksi'] = self.env['ir.sequence'].next_by_code('seq_cc') or _('New')

        onchanges = self._get_onchange_create()
        for onchange_method, changed_fields in onchanges.items():
            if any(f not in vals for f in changed_fields):
                invoice = self.new(vals)
                getattr(invoice, onchange_method)()
                for field in changed_fields:
                    if field not in vals and invoice[field]:
                        vals[field] = invoice._fields[field].convert_to_write(invoice[field], invoice)
        bank_account = self._get_default_bank_id(vals.get('type'), vals.get('company_id'))
        if bank_account and not vals.get('partner_bank_id'):
            vals['partner_bank_id'] = bank_account.id

        invoice = super(AccountInvoice, self.with_context(mail_create_nolog=True)).create(vals)

        if any(line.invoice_line_tax_ids for line in invoice.invoice_line_ids) and not invoice.tax_line_ids:
            invoice.compute_taxes()

        return invoice

    @api.one
    @api.depends('invoice_line__bill_ids.price_subtotal',
                 'currency_id', 'company_id', 'date_invoice', 'type', 'date')
    def _compute_amount_bill(self):
        round_curr = self.currency_id.round
        self.amount_untaxed_bill = sum(line.price_subtotal for line in self.invoice_line__bill_ids)
        self.amount_tax_bill = sum(round_curr(line.price_tax) for line in self.invoice_line__bill_ids)
        self.amount_total_bill = self.amount_untaxed_bill + self.amount_tax_bill
        # amount_total_company_signed = self.amount_total
        # amount_untaxed_signed = self.amount_untaxed
        # if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
        #     currency_id = self.currency_id
        #     rate_date = self._get_currency_rate_date() or fields.Date.today()
        #     amount_total_company_signed = currency_id._convert(self.amount_total, self.company_id.currency_id, self.company_id, rate_date)
        #     amount_untaxed_signed = currency_id._convert(self.amount_untaxed, self.company_id.currency_id, self.company_id, rate_date)
        # sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        # self.amount_total_company_signed = amount_total_company_signed * sign
        # self.amount_total_signed = self.amount_total * sign
        # self.amount_untaxed_signed = amount_untaxed_signed * sign
    @api.one
    @api.depends('amount_total_bill','amount_total')
    def _compute_selisih(self):
        self.amount_total_selisih = self.amount_total_bill - self.amount_total

    @api.one
    @api.depends('origin')
    def _compute_origin(self):
        if self.origin:
            purchase = self.env['purchase.order'].search([('name', '=', self.origin)])
            service = self.env['tbl_service_receipt'].search([('origin', '=', self.origin)], limit=1, order='id desc')
            if purchase:
                avail_po_value = 0
                for line in purchase.order_line:
                    avail = 0
                    avail = (line.product_qty - line.qty_invoiced)*line.price_unit
                    avail_po_value += avail
                self.avail_po_value = avail_po_value
            if service:
                journal_service = self.env['account.move'].search([('ref', '=', service.name)], limit=1, order='id desc')
                if journal_service:
                    self.journal_service = journal_service.id

    @api.onchange('purchase_id')
    def purchase_order_change(self):
        if not self.purchase_id:
            return {}
        if not self.partner_id:
            self.partner_id = self.purchase_id.partner_id.id

        vendor_ref = self.purchase_id.partner_ref
        if vendor_ref and (not self.reference or (
                vendor_ref + ", " not in self.reference and not self.reference.endswith(vendor_ref))):
            self.reference = ", ".join([self.reference, vendor_ref]) if self.reference else vendor_ref

        if not self.invoice_line_ids:
            #as there's no invoice line yet, we keep the currency of the PO
            self.currency_id = self.purchase_id.currency_id

        new_lines = self.env['account.invoice.line']
        new_lines1 = self.env['tbl_invoice_line']
        for line in self.purchase_id.order_line - self.invoice_line_ids.mapped('purchase_line_id'):
            data = self._prepare_invoice_line_from_po_line(line)
            new_line = new_lines.new(data)
            new_line._set_additional_fields(self)
            new_lines += new_line
            new_line1 = new_lines1.new(data)
            new_line1._set_additional_fields(self)
            new_lines1 += new_line1

        self.invoice_line_ids += new_lines
        self.invoice_line__bill_ids += new_lines1
        self.payment_term_id = self.purchase_id.payment_term_id
        self.env.context = dict(self.env.context, from_purchase_order_change=True)
        self.purchase_id = False
        return {}

    @api.multi
    def action_invoice_open(self):
        if self.amount_total_selisih == 0:
        # lots of duplicate calls to action_invoice_open, so we remove those already open
            to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
            if to_open_invoices.filtered(lambda inv: not inv.partner_id):
                raise UserError(_("The field Vendor is required, please complete it to validate the Vendor Bill."))
            if to_open_invoices.filtered(lambda inv: inv.state != 'draft'):
                raise UserError(_("Invoice must be in draft state in order to validate it."))
            if to_open_invoices.filtered(lambda inv: float_compare(inv.amount_total, 0.0, precision_rounding=inv.currency_id.rounding) == -1):
                raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
            if to_open_invoices.filtered(lambda inv: not inv.account_id):
                raise UserError(_('No account was found to create the invoice, be sure you have installed a chart of account.'))
            to_open_invoices.action_date_assign()
            to_open_invoices.action_move_create()
            return to_open_invoices.invoice_validate()
        else:
            self.state = 'approve'

    @api.multi
    def action_invoice_approve(self):
          compose_form = self.env.ref('msi_accounting.msi_sel_inv_wizard_form', False)
          return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'msi_sel_inv',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            # 'context': ctx,
          }

    @api.multi
    def action_invoice_approve2(self):
        # lots of duplicate calls to action_invoice_open, so we remove those already open
        to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
        if to_open_invoices.filtered(lambda inv: not inv.partner_id):
            raise UserError(_("The field Vendor is required, please complete it to validate the Vendor Bill."))
        # if to_open_invoices.filtered(lambda inv: inv.state != 'draft'):
        #     raise UserError(_("Invoice must be in draft state in order to validate it."))
        if to_open_invoices.filtered(lambda inv: float_compare(inv.amount_total, 0.0, precision_rounding=inv.currency_id.rounding) == -1):
            raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
        if to_open_invoices.filtered(lambda inv: not inv.account_id):
            raise UserError(_('No account was found to create the invoice, be sure you have installed a chart of account.'))
        to_open_invoices.action_date_assign()
        to_open_invoices.action_move_create()
        if self.amount_total_selisih != 0:
            self.action_update_journal_service()
        return to_open_invoices.invoice_validate()

    @api.multi
    def act_validate(self):
        if self.amount_total_selisih != 0:
          compose_form = self.env.ref('msi_accounting.msi_sel_inv_wizard_form', False)
          return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'msi_sel_inv',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            # 'context': ctx,
          }
        else:
          self.action_invoice_open()

    @api.multi
    def action_invoice_cancel(self):
        self.action_del_payment()
        return self.filtered(lambda inv: inv.state != 'cancel').action_cancel()

    @api.multi
    def action_del_payment(self):
        if self.payment_ids:
            for pay in self.payment_ids:
                payment = self.env['account.payment'].search([('id', '=', pay.id)])
                for bayar in payment:
                    if bayar.state not in ('posted','sent','reconciled'):
                        bayar.unlink()
                    else:
                        raise UserError(_('Payment %s sudah Paid/Reconcile' % (bayar.name, )))


    @api.multi
    def action_update_journal_service(self):
        account_move_line_obj = self.env['account.move.line']
        if self.journal_service:
            self.journal_service.button_cancel()
            if self.journal_service.line_ids:
                self.journal_service.line_ids.unlink()

            for line in self.invoice_line_ids:
              if line.is_service == True:
                data4 = account_move_line_obj.with_context(check_move_validity=False).create({
                    'name': line.product_id.name,
                    'date': self.journal_service.date,
                    'partner_id': self.partner_id.id,
                    'journal_id': line.product_id.categ_id.property_service_journal.id,
                    'account_id': line.product_id.property_account_expense_id.id or line.product_id.categ_id.property_account_expense_categ_id.id,
                    'move_id': self.journal_service.id,
                    'date_maturity': fields.Date.today(),
                    'debit': line.price_subtotal,
                })
          
                data3 = account_move_line_obj.with_context(check_move_validity=False).create({
                    'name': line.product_id.name,
                    'date': self.journal_service.date,
                    'partner_id': self.partner_id.id,
                    'journal_id': line.product_id.categ_id.property_service_journal.id,
                    'account_id': line.product_id.categ_id.property_service_account_input_categ_id.id,
                    'move_id': self.journal_service.id,
                    'date_maturity': fields.Date.today(),
                    'credit': line.price_subtotal,
                })

            self.journal_service.post()


class tbl_invoice_line(models.Model):
    _name = "tbl_invoice_line"
    _description = "Invoice Line Bill"
    # _order = "invoice_id,sequence,id"

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
        'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
        'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        currency = self.invoice_id and self.invoice_id.currency_id or None
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(price, currency, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
        self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else self.quantity * price
        self.price_total = taxes['total_included'] if taxes else self.price_subtotal
        if self.invoice_id.currency_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            currency = self.invoice_id.currency_id
            date = self.invoice_id._get_currency_rate_date()
            price_subtotal_signed = currency._convert(price_subtotal_signed, self.invoice_id.company_id.currency_id, self.company_id or self.env.user.company_id, date or fields.Date.today())
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign

    @api.model
    def _default_account(self):
        journal_id = self._context.get('journal_id') or self._context.get('default_journal_id')
        if journal_id:
            journal = self.env['account.journal'].browse(journal_id)
            if self._context.get('type') in ('out_invoice', 'in_refund'):
                return journal.default_credit_account_id.id
            return journal.default_debit_account_id.id

    def _get_price_tax(self):
        for l in self:
            l.price_tax = l.price_total - l.price_subtotal

    name = fields.Text(string='Description', required=True)
    origin = fields.Char(string='Source Document',
        help="Reference of the document that produced this invoice.")
    sequence = fields.Integer(default=10,
        help="Gives the sequence of this line when displaying the invoice.")
    invoice_id = fields.Many2one('account.invoice', string='Invoice Reference',
        ondelete='cascade', index=True)
    invoice_type = fields.Selection(related='invoice_id.type', readonly=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure',
        ondelete='set null', index=True, oldname='uos_id')
    product_id = fields.Many2one('product.product', string='Product',
        ondelete='restrict', index=True)
    product_image = fields.Binary('Product Image', related="product_id.image", store=False, readonly=True)
    account_id = fields.Many2one('account.account', string='Account', domain=[('deprecated', '=', False)],
        default=_default_account,
        help="The income or expense account related to the selected product.")
    price_unit = fields.Float(string='Unit Price', required=True, digits=dp.get_precision('Product Price'))
    price_subtotal = fields.Monetary(string='Amount (without Taxes)',
        store=True, readonly=True, compute='_compute_price', help="Total amount without taxes")
    price_total = fields.Monetary(string='Amount (with Taxes)',
        store=True, readonly=True, compute='_compute_price', help="Total amount with taxes")
    price_subtotal_signed = fields.Monetary(string='Amount Signed', currency_field='company_currency_id',
        store=True, readonly=True, compute='_compute_price',
        help="Total amount in the currency of the company, negative for credit note.")
    price_tax = fields.Monetary(string='Tax Amount', compute='_get_price_tax', store=False)
    quantity = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'),
        required=True, default=1)
    discount = fields.Float(string='Discount (%)', digits=dp.get_precision('Discount'),
        default=0.0)
    invoice_line_tax_ids = fields.Many2many('account.tax',
        # 'account_invoice_line_tax', 'invoice_line_id', 'tax_id',
        string='Taxes', domain=[('type_tax_use','!=','none'), '|', ('active', '=', False), ('active', '=', True)], oldname='invoice_line_tax_id')
    account_analytic_id = fields.Many2one('account.analytic.account',
        string='Analytic Account')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    company_id = fields.Many2one('res.company', string='Company',
        related='invoice_id.company_id', store=True, readonly=True, related_sudo=False)
    partner_id = fields.Many2one('res.partner', string='Partner',
        related='invoice_id.partner_id', store=True, readonly=True, related_sudo=False)
    currency_id = fields.Many2one('res.currency', related='invoice_id.currency_id', store=True, related_sudo=False, readonly=False)
    company_currency_id = fields.Many2one('res.currency', related='invoice_id.company_currency_id', readonly=True, related_sudo=False)
    is_rounding_line = fields.Boolean(string='Rounding Line', help='Is a rounding line in case of cash rounding.')

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")

    purchase_line_bill_id = fields.Many2one('purchase.order.line', 'Purchase Order Line', ondelete='set null', index=True, readonly=True)

    is_service = fields.Boolean(string='Is Service')

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(tbl_invoice_line, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if self._context.get('type'):
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='product_id']"):
                if self._context['type'] in ('in_invoice', 'in_refund'):
                    # Hack to fix the stable version 8.0 -> saas-12
                    # purchase_ok will be moved from purchase to product in master #13271
                    if 'purchase_ok' in self.env['product.template']._fields:
                        node.set('domain', "[('purchase_ok', '=', True)]")
                else:
                    node.set('domain', "[('sale_ok', '=', True)]")
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res

    @api.v8
    def get_invoice_line_account(self, type, product, fpos, company):
        accounts = product.product_tmpl_id.get_product_accounts(fpos)
        if type in ('out_invoice', 'out_refund'):
            return accounts['income']
        return accounts['expense']

    def _set_currency(self):
        company = self.invoice_id.company_id
        currency = self.invoice_id.currency_id
        if company and currency:
            if company.currency_id != currency:
                self.price_unit = self.price_unit * currency.with_context(dict(self._context or {}, date=self.invoice_id.date_invoice)).rate

    def _set_taxes(self):
        """ Used in on_change to set taxes and price"""
        self.ensure_one()

        # Keep only taxes of the company
        company_id = self.company_id or self.env.user.company_id

        if self.invoice_id.type in ('out_invoice', 'out_refund'):
            taxes = self.product_id.taxes_id.filtered(lambda r: r.company_id == company_id) or self.account_id.tax_ids or self.invoice_id.company_id.account_sale_tax_id
        else:
            taxes = self.product_id.supplier_taxes_id.filtered(lambda r: r.company_id == company_id) or self.account_id.tax_ids or self.invoice_id.company_id.account_purchase_tax_id

        self.invoice_line_tax_ids = fp_taxes = self.invoice_id.fiscal_position_id.map_tax(taxes, self.product_id, self.invoice_id.partner_id)

        fix_price = self.env['account.tax']._fix_tax_included_price
        if self.invoice_id.type in ('in_invoice', 'in_refund'):
            prec = self.env['decimal.precision'].precision_get('Product Price')
            if not self.price_unit or float_compare(self.price_unit, self.product_id.standard_price, precision_digits=prec) == 0:
                self.price_unit = fix_price(self.product_id.standard_price, taxes, fp_taxes)
                self._set_currency()
        else:
            self.price_unit = fix_price(self.product_id.lst_price, taxes, fp_taxes)
            self._set_currency()

    @api.onchange('product_id')
    def _onchange_product_id(self):
        domain = {}
        if not self.invoice_id:
            return

        part = self.invoice_id.partner_id
        fpos = self.invoice_id.fiscal_position_id
        company = self.invoice_id.company_id
        currency = self.invoice_id.currency_id
        type = self.invoice_id.type

        if not part:
            warning = {
                    'title': _('Warning!'),
                    'message': _('You must first select a partner.'),
                }
            return {'warning': warning}

        if not self.product_id:
            if type not in ('in_invoice', 'in_refund'):
                self.price_unit = 0.0
            domain['uom_id'] = []
            if fpos:
                self.account_id = fpos.map_account(self.account_id)
        else:
            self_lang = self
            if part.lang:
                self_lang = self.with_context(lang=part.lang)

            product = self_lang.product_id
            account = self.get_invoice_line_account(type, product, fpos, company)
            if account:
                self.account_id = account.id
            self._set_taxes()

            product_name = self_lang._get_invoice_line_name_from_product()
            if product_name != None:
                self.name = product_name

            if not self.uom_id or product.uom_id.category_id.id != self.uom_id.category_id.id:
                self.uom_id = product.uom_id.id
            domain['uom_id'] = [('category_id', '=', product.uom_id.category_id.id)]

            if company and currency:

                if self.uom_id and self.uom_id.id != product.uom_id.id:
                    self.price_unit = product.uom_id._compute_price(self.price_unit, self.uom_id)
        return {'domain': domain}

    def _get_invoice_line_name_from_product(self):
        """ Returns the automatic name to give to the invoice line depending on
        the product it is linked to.
        """
        self.ensure_one()
        if not self.product_id:
            return ''
        invoice_type = self.invoice_id.type
        rslt = self.product_id.partner_ref
        if invoice_type in ('in_invoice', 'in_refund'):
            if self.product_id.description_purchase:
                rslt += '\n' + self.product_id.description_purchase
        else:
            if self.product_id.description_sale:
                rslt += '\n' + self.product_id.description_sale

        return rslt

    @api.onchange('account_id')
    def _onchange_account_id(self):
        if not self.account_id:
            return
        if not self.product_id:
            fpos = self.invoice_id.fiscal_position_id
            if self.invoice_id.type in ('out_invoice', 'out_refund'):
                default_tax = self.invoice_id.company_id.account_sale_tax_id
            else:
                default_tax = self.invoice_id.company_id.account_purchase_tax_id
            self.invoice_line_tax_ids = fpos.map_tax(self.account_id.tax_ids or default_tax, partner=self.partner_id)
        elif not self.price_unit:
            self._set_taxes()


    @api.onchange('uom_id')
    def _onchange_uom_id(self):
        warning = {}
        result = {}
        if not self.uom_id:
            self.price_unit = 0.0

        if self.product_id and self.uom_id:
            self._set_taxes()
            self.price_unit = self.product_id.uom_id._compute_price(self.price_unit, self.uom_id)

            if self.product_id.uom_id.category_id.id != self.uom_id.category_id.id:
                warning = {
                    'title': _('Warning!'),
                    'message': _('The selected unit of measure has to be in the same category as the product unit of measure.'),
                }
                self.uom_id = self.product_id.uom_id.id
        if warning:
            result['warning'] = warning
        return result

    def _set_additional_fields(self, invoice):
        """ Some modules, such as Purchase, provide a feature to add automatically pre-filled
            invoice lines. However, these modules might not be aware of extra fields which are
            added by extensions of the accounting module.
            This method is intended to be overridden by these extensions, so that any new field can
            easily be auto-filled as well.
            :param invoice : account.invoice corresponding record
            :rtype line : account.invoice.line record
        """
        pass

    @api.multi
    def unlink(self):
        if self.filtered(lambda r: r.invoice_id and r.invoice_id.state != 'draft'):
            raise UserError(_('You can only delete an invoice line if the invoice is in draft state.'))
        return super(tbl_invoice_line, self).unlink()

    def _prepare_invoice_line(self):
        data = {
            'name': self.name,
            'origin': self.origin,
            'uom_id': self.uom_id.id,
            'product_id': self.product_id.id,
            'account_id': self.account_id.id,
            'price_unit': self.price_unit,
            'quantity': self.quantity,
            'discount': self.discount,
            'account_analytic_id': self.account_analytic_id.id,
            'analytic_tag_ids': self.analytic_tag_ids.ids,
            'invoice_line_tax_ids': self.invoice_line_tax_ids.ids
        }
        return data

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('display_type', self.default_get(['display_type'])['display_type']):
                vals.update(price_unit=0, account_id=False, quantity=0)
        return super(tbl_invoice_line, self).create(vals_list)

    @api.multi
    def write(self, values):
        if 'display_type' in values and self.filtered(lambda line: line.display_type != values.get('display_type')):
            raise UserError(_("You cannot change the type of an invoice line. Instead you should delete the current line and create a new line of the proper type."))
        return super(tbl_invoice_line, self).write(values)

    _sql_constraints = [
        ('accountable_required_fields',
            "CHECK(display_type IS NOT NULL OR account_id IS NOT NULL)",
            "Missing required account on accountable invoice line."),

        ('non_accountable_fields_null',
            "CHECK(display_type IS NULL OR (price_unit = 0 AND account_id IS NULL and quantity = 0))",
            "Forbidden unit price, account and quantity on non-accountable invoice line"),
    ]


class account_payment(models.Model):
    _inherit = "account.payment"

    communication1 = fields.Char('Memo')
    communication = fields.Char(string='Code Transaksi')

    @api.model
    def default_get(self, fields):
        rec = super(account_payment, self).default_get(fields)
        invoice_defaults = self.resolve_2many_commands('invoice_ids', rec.get('invoice_ids'))
        if invoice_defaults and len(invoice_defaults) == 1:
            invoice = invoice_defaults[0]
            rec['communication'] = invoice['code_transaksi']
            rec['communication1'] = invoice['reference'] or invoice['name'] or invoice['number']
            rec['currency_id'] = invoice['currency_id'][0]
            rec['payment_type'] = invoice['type'] in ('out_invoice', 'in_refund') and 'inbound' or 'outbound'
            rec['partner_type'] = MAP_INVOICE_TYPE_PARTNER_TYPE[invoice['type']]
            rec['partner_id'] = invoice['partner_id'][0]
            rec['amount'] = invoice['residual']
        return rec

class account_bank_statement_line(models.Model):
    _inherit = "account.bank.statement.line"

    name = fields.Char(string='Reconcile Code', required=True)
    name1 = fields.Char(string='Label', required=True)

class tbl_msi_accounting_from_purchase_line(models.Model):
    _inherit = "purchase.order.line"

    invoice_bill_lines = fields.One2many('tbl_invoice_line', 'purchase_line_bill_id', string="Bill Lines", readonly=True, copy=False)


class msi_sel_inv(models.TransientModel):
    _name = 'msi_sel_inv'

    def act_yes(self):
        leads = self.env['account.invoice'].browse(self.env.context.get('active_ids'))
        if leads.state == 'draft':
            leads.action_invoice_open()
        else:
            leads.action_invoice_approve2()

class msi_accounting_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    is_service = fields.Boolean(string='Is Service')