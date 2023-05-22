from lxml import etree
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import email_re, email_split, email_escape_char, float_is_zero, float_compare, \
    pycompat, date_utils
from odoo.exceptions import UserError, AccessError
import xlsxwriter
import base64
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from calendar import monthrange

import math

class purchase_oder(models.Model):

    _inherit = "purchase.order"

    data = fields.Binary(string='File', readonly=True)

    @api.multi
    def print_xls_report(self):
      if self.order_line:
        xls_filename =str(self.name)+'.xlsx'
        workbook = xlsxwriter.Workbook('/tmp/' + xls_filename)
        # report_sales_ete_detail_obj = self.env['report.eq_inventory_valuation_report.inventory_valuation_report']
        header_merge_format = workbook.add_format({'bold':True, 'align':'center', 'valign':'vcenter', \
                                            'font_size':10, 'border':1})

        header_data_format = workbook.add_format({'align':'center', 'valign':'vcenter', \
                                                   'font_size':10, 'border':1})
        product_header_format = workbook.add_format({'valign':'vleft', 'font_size':10, 'border':0})
        rows = 8
        no = 1
        worksheet = workbook.add_worksheet(self.name)

        # worksheet.write(0,0, self.name.name, product_header_format)

        worksheet.write(7,0, 'No', header_merge_format)
        worksheet.write(7,1, 'Part Number', header_merge_format)
        worksheet.write(7,2, 'Description', header_merge_format)
        worksheet.write(7,3, 'Keterangan', header_merge_format)
        worksheet.write(7,4, 'Part Number Subtitusi', header_merge_format)
        worksheet.write(7,5, 'Poisi Stock Vendor', header_merge_format)
        worksheet.write(7,6, 'Harga', header_merge_format)
        worksheet.write(7,7, 'Estimasi Delivery Onsite', header_merge_format)
        for line in self.order_line:
            worksheet.write(rows,0, no, header_data_format)
            worksheet.write(rows,1, line.product_id.default_code, header_data_format)
            worksheet.write(rows,2, line.product_id.name, header_data_format)
            worksheet.write(rows,3, '', header_data_format)
            worksheet.write(rows,4, '', header_data_format)
            worksheet.write(rows,5, '', header_data_format)
            worksheet.write(rows,6, '', header_data_format)
            worksheet.write(rows,7, '', header_data_format)
            rows += 1
            no += 1
        workbook.close()
        self.write({
            # 'state': 'get',
            'data': base64.b64encode(open('/tmp/' + xls_filename, 'rb').read()),
            # 'name': xls_filename
        })
    
    def action_print(self):
        return self.env.ref('bisa_purchase_order.action_report_purchase_order').report_action(self)
    
