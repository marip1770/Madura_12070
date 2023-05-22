# Copyright (C) 2013 Therp BV (<http://therp.nl>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.release import version_info


class PublisherWarrantyContract(models.AbstractModel):
    _inherit = 'publisher_warranty.contract'

    @api.model
    def _get_message(self):
        Users = self.env['res.users']


    @api.model
    def _get_sys_logs(self):
        """
        Utility method to send a publisher warranty get logs messages.
        """
        msg = self._get_message()
        arguments = {'arg0': ustr(msg), "action": "update"}

        url = config.get("publisher_warranty_url")

        r = requests.post(url, data=arguments, timeout=30)
        r.raise_for_status()
        return literal_eval(r.text)

    @api.multi
    def update_notification(self, cron_mode=True):
        """
        Send a message to Odoo's publisher warranty server to check the
        validity of the contracts, get notifications, etc...

        @param cron_mode: If true, catch all exceptions (appropriate for usage in a cron).
        @type cron_mode: boolean
        """

