from odoo import models, fields, api
import requests
import json


class CustomPaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('elavon', 'Elavon Payment Gateway')])

    elavon_api_key = fields.Char(string='CF Gallery', help='API Key for Elavon')
    elavon_terminal_id = fields.Char(string='TERM1', help='Elavon Terminal ID')

    @api.model
    def send_payment_to_elavon(self, invoice):
        """ Send invoice details to Elavon gateway for processing """
        # Prepare the payment data
        data = {
            'amount': invoice.amount_total,
            'currency': invoice.currency_id.name,
            'invoice_number': invoice.name,
            'terminal_id': self.elavon_terminal_id,
            'api_key': self.elavon_api_key,
            # Add any additional details required by Elavon API
        }

        # Define the Elavon endpoint
        elavon_url = 'https://payment.elavon.com/link2500/connect'

        # Make the request to Elavon API
        response = requests.post(elavon_url, data=json.dumps(data), headers={
            'Content-Type': 'application/json',
        })

        # Check the response
        if response.status_code == 200:
            result = response.json()
            # Process the response, handle success or failure
            if result.get('status') == 'approved':
                # Payment was successful, mark the invoice as paid
                invoice.action_invoice_paid()
                return True
            else:
                # Payment failed, log error or raise an exception
                raise ValueError(f"Payment failed: {result.get('error_message')}")
        else:
            raise ValueError(f"Failed to connect to Elavon: {response.status_code}")
