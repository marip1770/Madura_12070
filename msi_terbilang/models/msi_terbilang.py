from odoo import fields, models, api, _
from odoo.exceptions import UserError

satuan = ['', 'satu ', 'dua ', 'tiga ', 'empat ', 'lima ',
          'enam ', 'tujuh ', 'delapan ', 'sembilan ', 'sepuluh ', 'sebelas ', 'dua belas ', 'tiga belas ',
          'empat belas ', 'lima belas ', 'enam belas ', 'tujuh belas ', 'delapan belas ', 'sembilan belas ']


class Currency(models.Model):
    _inherit = 'res.currency'

    def tulis(self, angka, kelipatan):
        terbilang = satuan[angka] + kelipatan
        return terbilang

    def ratus_puluh_satuan(self, angka):
        ratus = angka // 100
        sisa_ratus = angka % 100
        puluh = sisa_ratus // 10
        satuan = angka % 10
        terbilang = ''

        if ratus == 1:
            terbilang += self.tulis(0, "seratus ")
        elif ratus != 1 and ratus >= 1:
            terbilang += self.tulis(ratus, "ratus ")
        if sisa_ratus >= 20:
            terbilang += self.tulis(puluh, "puluh ")
            terbilang += self.tulis(satuan, "")
        elif sisa_ratus < 20:
            terbilang += self.tulis(sisa_ratus, "")

        return terbilang

    def milyar_juta_ribu(self, angka):
        milyar = angka // 1000000000
        sisa_milyar = angka % 1000000000
        juta = sisa_milyar // 1000000
        sisa_juta = sisa_milyar % 1000000
        ribu = sisa_juta // 1000
        sisa_ribu = sisa_juta % 1000
        terbilang = ''

        if milyar >= 1:
            terbilang += self.ratus_puluh_satuan(milyar)
            terbilang += "milyar "
        if juta >= 1:
            terbilang += self.ratus_puluh_satuan(juta)
            terbilang += "juta "
        if ribu > 1:
            terbilang += self.ratus_puluh_satuan(ribu)
            terbilang += "ribu "
        elif ribu == 1:
            terbilang += "seribu "
        terbilang += self.ratus_puluh_satuan(sisa_ribu)
        terbilang = terbilang #+ "Rupiah"
        return terbilang.upper()


class msi_account_invoice(models.Model):
    _inherit = "account.invoice"

    terbilang = fields.Char(string="Terbilang :", compute="_compute_terbilang", required=False )

    @api.one
    @api.depends('amount_total')
    def _compute_terbilang(self):
        for r in self:
            if r.amount_total:
                r.terbilang = r.currency_id.milyar_juta_ribu(int(r.amount_total))


class msi_account_payment_terbilang(models.Model):
    _inherit = "account.payment"

    terbilang = fields.Char(string="Terbilang :", compute="_compute_terbilang", required=False )

    @api.one
    @api.depends('amount')
    def _compute_terbilang(self):
        for r in self:
            if r.amount:
                r.terbilang = r.currency_id.milyar_juta_ribu(int(r.amount))
