from odoo import models, fields, api
import requests

class IngenicoDevice(models.Model):
    _name = 'ingenico.device'
    _description = 'Ingenico Device'

    name = fields.Char(string="Device Name", required=True)
    pairing_code = fields.Char(string="Pairing Code", required=True)
    company_name = fields.Char(string="Company Name", required=True)
    status = fields.Selection(
        [('paired', 'Paired'), ('unpaired', 'Unpaired')],
        string="Status",
        default='unpaired',
    )

    @api.model
    def pair_device(self, pairing_code, company_name):
        url = "https://uat.pos.hpi.elavonaws.com/devices"
        payload = {
            "pairing_code": pairing_code,
            "company_name": company_name
        }
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to pair device: {response.text}")
        except Exception as e:
            return {"error": str(e)}
