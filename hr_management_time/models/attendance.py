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


class tbl_msi_attendance(models.Model):
    _name = 'tbl_msi_attendance'
    _description = "Attendance"
    _order = 'tgl_jam desc'
   
    name = fields.Char('NIK')
    nik = fields.Char('NIK', compute='_compute_nik', store=True)
    date = fields.Date('Date')
    time = fields.Char('Time HH:MM')
    time2 = fields.Char('Time HH:MM')
    tgl_jam = fields.Datetime('Tgl_jam', compute='_tgl_jam', store=True)


    @api.one
    @api.depends('date','time')
    def _tgl_jam(self):
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        TIME_FORMAT = "%H:%M:%S"

        if self. date:
           if self.time:
              str_ret_time = str(self.time) + ":00"
              str_ret_time = datetime.strptime(str_ret_time, TIME_FORMAT).time()
              jam = (datetime.combine(self.date,str_ret_time)) - timedelta(hours=7)
              self.tgl_jam = jam

           if not self.time:
              str_ret_time = "00:01:00"
              str_ret_time = datetime.strptime(str_ret_time, TIME_FORMAT).time()
              jam = (datetime.combine(self.date,str_ret_time)) - timedelta(hours=7)
              self.tgl_jam = jam

    @api.one
    @api.depends('name')
    def _compute_nik(self):
        if self.name:
          self.nik = str(self.name).strip()