from odoo import models, fields, api

class AuthenticationWizard(models.TransientModel):
    _name = "authentication.wizard"
    _description = "Authentication Setup Wizard"

    username = fields.Char("Username", required=True)
    password = fields.Char("Password", required=True)

    def save_authentication(self):
        self.env['authentication.conf'].set_authentication_credentials(self.username, self.password)
        return {'type': 'ir.actions.act_window_close'}
