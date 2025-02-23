import requests

from odoo import models, fields, api

class AuthenticationConfig(models.Model):
    _name = "authentication.conf"
    _description = "Authentication Configuration"

    username = fields.Char("Username", required=True)
    password = fields.Char("Password", required=True, password=True)
    # token = fields.Char("Token", readonly=True)

    @api.model
    def set_authentication_credentials(self, username, password):
        """Save authentication credentials in system parameters"""
        self.env['ir.config_parameter'].sudo().set_param('authentication.username', username)
        self.env['ir.config_parameter'].sudo().set_param('authentication.password', password)

    @api.model
    def get_authentication_credentials(self):
        """Retrieve authentication credentials"""
        username = self.env['ir.config_parameter'].sudo().get_param('authentication.username', default='')
        password = self.env['ir.config_parameter'].sudo().get_param('authentication.password', default='')
        return username, password


    @api.model
    def generate_token(self, username, password):
        # Simulate calling an external API for token generation
        url = "https://uat.pos.hpi.elavonaws.com/credentials/token"
        payload = {"Username": username, "Password": password}
        headers = {
            "Content-Type": "application/json",
            "Accept-Version": "V2",
            "Accept": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            token = response.json().get("token")
            return token
        else:
            return False

    @api.model
    def authenticate_user(self, vals):
        username = vals.get("username")
        password = vals.get("password")

        token = self.generate_token(username, password)
        if token:
            return {"status": "success", "token": token}
        else:
            return {"status": "error", "message": "Invalid credentials"}
