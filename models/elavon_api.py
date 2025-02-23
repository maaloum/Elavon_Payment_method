from odoo import models, fields, api
import requests


class ElavonAPI(models.Model):
    _name = 'elavon.api'
    _description = 'Elavon API Integration'

    name = fields.Char(string="API Name")
    base_url = fields.Char(string="API Base URL", default="https://test.api.elavon.com")
    client_id = fields.Char(string="Client ID")
    client_secret = fields.Char(string="Client Secret")

    def get_access_token(self):
        url = f"{self.base_url}/oauth/token"
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            raise Exception("Failed to obtain access token")

    def process_payment(self, amount, currency):
        token = self.get_access_token()
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        url = f"{self.base_url}/cpi/transactions"
        payload = {
            "transaction": {
                "amount": amount,
                "currency": currency,
                "transactionType": "SALE",
            }
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
