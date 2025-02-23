import requests
import logging

from odoo import models, api

_logger = logging.getLogger(__name__)
class TransactionManager(models.Model):
    _name = "transaction.manager"
    _description = "Transaction Manager for Elavon API"
    @api.model
    def send_refund(self):
        """Send a refund transaction and refresh token if expired."""
        config = self.env['ir.config_parameter'].sudo()
        token = config.get_param('authentication_conf')

        # Retrieve a new token if none exists
        if not token:
            token = self.env["authentication.manager"].get_token()
            config.set_param('authentication_conf', token)

        headers = {
            "Content-Type": "application/vnd.elavon.transaction-b.v1+json",
            "Accept-Version": "V2",
            "Authorization": f"Bearer {token}"
        }

        url = "https://uat.pos.hpi.elavonaws.com/devices/XrkYrftYmyXGp2fb/message"
        data = {
            "messageId": "unique-transaction-id-12345",
            "responseChannelType": "SYNCHRONOUS",
            "responseChannel": {
                "responsePayloadFormat": "DEVICEMESSAGE"
            },
            "messageType": "application/vnd.elavon.transaction-b.v1+json",
            "message": {
                "referenceNumber": "12346001",
                "identifiers": {
                    "chain": "TSTLA3",
                    "location": "CFGALLERY",
                    "terminal": "TERM1"
                },
                "transType": "REFUND",
                "transAmount": "10.00",
                "manuallyEntered": "FALSE",
                "partialAuthFlag": "1",
                "uniqueDeviceId": "11223344",
                "transactionDateTime": "2025-01-25T03:44:24.770Z",
                "cashierId": "12340110",
                "userDefinedData": "123456",
                "compliance": {
                    "uniqueLaneId": "09033243",
                    "customerCode": "00702011"
                }
            }
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            # If token expired (HTTP 401), refresh token and retry
            if e.response is not None and e.response.status_code == 401:
                _logger.info("Token expired. Refreshing token...")
                token = self.env["authentication.manager"].get_token()
                config.set_param('elavon_api_token', token)
                headers["Authorization"] = f"Bearer {token}"
                try:
                    response = requests.post(url, headers=headers, json=data, timeout=10)
                    response.raise_for_status()
                    return response.json()
                except requests.exceptions.RequestException as ex:
                    _logger.error("Refund retry failed: %s", ex)
                    raise ValueError(f"Refund request failed after token refresh: {ex}")
            else:
                _logger.error("Refund request failed: %s", e)
                raise ValueError(f"Refund request failed: {str(e)}")
        except requests.exceptions.RequestException as e:
            _logger.error("Refund request encountered an error: %s", e)
            raise ValueError(f"Refund request encountered an error: {str(e)}")