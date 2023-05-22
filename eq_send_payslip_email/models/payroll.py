# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class hr_payslip(models.Model):
    _name = 'hr.payslip'
    _inherit = ['hr.payslip', 'mail.thread']

    @api.multi
    def action_payslip_sent(self):
        self.ensure_one()
        template = self.env.ref('eq_send_payslip_email.email_template_payslip', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        lang = self.env.context.get('lang')
        if template and template.lang:
            lang = template._render_template(template.lang, 'hr.payslip', self.id)
        self = self.with_context(lang=lang)
        ctx = {
            'default_model': 'hr.payslip',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template.id),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'model_description': "Payslip",
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }


class hr_payslip_run(models.Model):
    _inherit = 'hr.payslip.run'

    @api.multi
    def action_batch_payslip_sent(self):
        return {
            'name': _('Send By Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.mass.send.payslip',
            'target': 'new',
        }


class wizard_mass_send_payslip(models.TransientModel):
    _name = 'wizard.mass.send.payslip'
    _description = "Wizard Mass Send Payslip"

    payslip_ids = fields.Many2many('hr.payslip', string="Payslip")

    @api.model
    def default_get(self, fieldslist):
        res = super(wizard_mass_send_payslip, self).default_get(fieldslist)
        context = self.env.context
        if context.get('active_model') == 'hr.payslip':
            res.update({'payslip_ids': [(6, 0, context['active_ids'])]})
        elif context.get('active_model') == 'hr.payslip.run':
            batch_id = self.env['hr.payslip.run'].browse(context['active_id'])
            res.update({'payslip_ids': [(6, 0, batch_id.slip_ids.ids)]})
        return res

    @api.multi
    def btn_mass_send_payslip(self):
        if not self.payslip_ids:
            return
        emp_without_workemail = []
        for payslip in self.payslip_ids:
            if payslip.state != 'done':
                raise ValidationError(_("Selected Payslip must be in Done state."))
            if not payslip.employee_id.work_email:
                emp_without_workemail.append(payslip.employee_id.name)
        if emp_without_workemail:
            emp_without_workemail = list(set(emp_without_workemail))
            raise ValidationError(_("""Please set the Work Email for below Employee(s).\n
                                    %s""") % ('\n'.join(map(str, emp_without_workemail))))
        compose_obj = self.env['mail.compose.message']
        all_fields = compose_obj._fields.keys()
        for payslip in self.payslip_ids:
            compose_vals = payslip.action_payslip_sent()
            default_vals = compose_obj.with_context(compose_vals['context']).default_get(all_fields)
            compose_id = compose_obj.create(default_vals)
            compose_id.onchange_template_id_wrapper()
            compose_id.action_send_mail()

    @api.multi
    def btn_template_preview(self):
        action = self.env.ref('mail.wizard_email_template_preview').read()[0]
        ctx = {'template_id': self.env.ref('eq_send_payslip_email.email_template_payslip').id}
        action['context'] = ctx
        return action

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: