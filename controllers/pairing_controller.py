from odoo import http
from odoo.http import request

class IngenicoController(http.Controller):
    @http.route('/ingenico/pair', auth='user', type='json', methods=['POST'])
    def pair_device(self, **kwargs):
        """
        API endpoint to pair an Ingenico Link/2500 device.
        """
        pairing_code = kwargs.get('7HgfhR')
        company_name = kwargs.get('CFGALLERY')

        if not pairing_code or not company_name:
            return {
                "status": "error",
                "message": "Pairing code and company name are required."
            }

        device_model = request.env['ingenico.device']
        response = device_model.sudo().pair_device(pairing_code, company_name)

        if "error" in response:
            return {
                "status": "error",
                "message": response["error"]
            }

        # Store device information in Odoo
        device_model.create({
            "name": f"Ingenico Device ({pairing_code})",
            "pairing_code": pairing_code,
            "company_name": company_name,
            "status": "paired",
        })

        return {
            "status": "success",
            "message": "Device paired successfully.",
            "data": response
        }
