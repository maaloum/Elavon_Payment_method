import base64
import requests
from odoo import http
from odoo.http import request

class ElavonAuthController(http.Controller):
    @http.route('/elavon/authenticate', auth='user', type='json', methods=['POST'])
    def authenticate(self, **kwargs):
        """
        Endpoint to authenticate with Elavon API and retrieve an access token.
        """
        conf = request.env['accounting.conf'].search([], limit=1)
        print("Confi", conf)
        if conf:
            client_id = conf.client_id
            client_secret = conf.client_secret
            token_url = conf.token_url
        # else:
        #     va

        # Credentials
        client_id = "v8rkb3whvy32ck4ctfrk9t22pdb2"
        client_secret = "hr2f8rfw666f9tmf8bfdbgvxtyy7"
        token_url = "https://uat.pos.hpi.elavonaws.com/credentials/token"

        # Base64 encode the credentials
        credentials = f"{client_id}:{client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        # Headers and body for the request
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "Accept-Version": "V2",
        }
        body = {
            "grant_type": "client_credentials"
        }

        try:
            # Make the request
            response = requests.post(token_url, headers=headers, data=body)
            if response.status_code == 200:
                # Parse the response
                token_data = response.json()
                return {
                    "status": "success",
                    "access_token": token_data.get("access_token"),
                    "expires_in": token_data.get("expires_in"),
                }
            else:
                return {
                    "status": "error",
                    "message": response.text,
                    "code": response.status_code,
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }
