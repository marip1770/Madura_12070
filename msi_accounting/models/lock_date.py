from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountChangeLockDate(models.TransientModel):
    """
    This wizard is used to change the lock date
    """
    _inherit = 'account.change.lock.date'

    pr_start_date = fields.Date(
        string='PR Start Date',
        default=lambda self: self.env.user.company_id.pr_start_date)
    pr_end_date = fields.Date(
        string='PR End Date',
        default=lambda self: self.env.user.company_id.pr_end_date)

    gr_start_date = fields.Date(
        string='GR Start Date',
        default=lambda self: self.env.user.company_id.gr_start_date)
    gr_end_date = fields.Date(
        string='GR End Date',
        default=lambda self: self.env.user.company_id.gr_end_date)

    closing_start_date = fields.Date(
        string='Closing Start Date',
        default=lambda self: self.env.user.company_id.closing_start_date)
    closing_end_date = fields.Date(
        string='Closing End Date',
        default=lambda self: self.env.user.company_id.closing_end_date)

    @api.multi
    def change_lock_date(self):
        self.env.user.company_id.write({'period_lock_date': self.period_lock_date, 
                                        'fiscalyear_lock_date': self.fiscalyear_lock_date, 
                                        'pr_start_date':self.pr_start_date, 
                                        'pr_end_date':self.pr_end_date, 
                                        'gr_start_date':self.gr_start_date, 
                                        'gr_end_date':self.gr_end_date,
                                        'closing_start_date':self.closing_start_date, 
                                        'closing_end_date':self.closing_end_date
                                        })
        return {'type': 'ir.actions.act_window_close'}

class Company(models.Model):
    _inherit = 'res.company'

    pr_start_date = fields.Date(
        string='PR Start Date')
    pr_end_date = fields.Date(
        string='PR End Date')
    gr_start_date = fields.Date(
        string='GR Start Date')
    gr_end_date = fields.Date(
        string='GR End Date')
    closing_start_date = fields.Date(
        string='Closing Start Date')
    closing_end_date = fields.Date(
        string='Closing End Date')

class PurchaseRequest(models.Model):

    _inherit = 'purchase.request'

    pr_start_date = fields.Date(
        string='PR Start Date',
        default=lambda self: self.env.user.company_id.pr_start_date)
    pr_end_date = fields.Date(
        string='PR End Date',
        default=lambda self: self.env.user.company_id.pr_end_date)

    # @api.model
    # def create(self, vals):
    #     res = super(PurchaseRequest, self).create(vals)
    #     if vals.get('assigned_to'):
    #         if vals['date_start'] >= self.pr_start_date and if vals['date_start'] <= self.pr_end_date :
    #             raise UserError(_("Tanggal Pengajuan Melebihi batas yang di tentukan"))
    #     else:
    #         if vals['date_start'] >= self.pr_start_date and if vals['date_start'] <= self.pr_end_date :
    #             raise UserError(_("Tanggal Pengajuan Melebihi batas yang di tentukan"))
    #     return res
    @api.model
    def create(self, vals):
        # if vals.get('name', _('New')) == _('New'):
        #         vals['name'] = self.env['ir.sequence'].next_by_code('lembur') or _('New')#
        if vals['date_start'] <= vals['pr_start_date'] or vals['date_start'] >= vals['pr_end_date'] :
                raise UserError(_("Tanggal Pengajuan Melebihi batas yang di tentukan"))
        result = super(PurchaseRequest, self).create(vals)
        return result