from odoo import models, fields, api
class AccountingConf(models.Model):
    _name = 'accounting.conf'

    name = fields.Char()
    company_id = fields.Many2one('res.company', string='Company', readonly=True,
                                 default=lambda self: self.env.company)
    client_id = fields.Char()
    client_secret = fields.Char()
    token_url = fields.Char()




