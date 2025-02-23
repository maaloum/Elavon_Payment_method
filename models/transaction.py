# import requests
# import json
# #
# # # Endpoint URL
# url = "https://uat.pos.hpi.elavonaws.com/devices/XrkYrftYmyXGp2fb/message"
#
# # Replace 'your_token_here' with the actual Bearer token
# token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ2OHJrYjN3aHZ5MzJjazRjdGZyazl0MjJwZGIyIiwiYXVkIjpbImhwaS5lbGF2b24uY29tIl0sInNjb3BlIjpbXSwiaXNzIjoiYzJvYXV0aCIsImV4cCI6MTc0MDM0NTUxMiwiYXV0aG9yaXRpZXMiOlsiY2VpOk1RbUtxOWJjbTRqZjhyNGQiXSwianRpIjoiMGVmOTNhYjYtYzE5ZS00ZmQyLThhOGItNGI2MzZkYzgwY2NiIiwiY2xpZW50X2lkIjoidjhya2Izd2h2eTMyY2s0Y3Rmcms5dDIycGRiMiJ9.lIqwUTNSUanxSSSU2SuJTu8aM8RjeTRI1sBZHhPl4ECxEB1FQjwLvHioOAggVMVUbpQIXWFzeXM0cUjeLoDq8DVYDffgDsiwxQIxxFWzKHBeohGiGWdS9Jyow7wnvvQFGatVRREZ4C6EF66W8W_CFfVqsPtiWD4kSk97KLrYB8zsXtuPb-e-Fm_2RCsvYH8xMa0dfe1uEU8atR7ZaPpgbIpBW892qE6p_QMwmXlFkaQ-UOoXw58CCbiVghl7feoXdXdas8x4QT3whgvHHiUZ1Bz2xQfO-3gz2Ij827EMEfJ1uMN2BqRN6diProZNrwRL3El6EBHWtzYEQ432kt-FOw"
# # Headers
# headers = {
#     "Content-Type": "application/vnd.elavon.transaction-b.v1+json",
#     "Accept-Version": "V2",
#     "Authorization": f"Bearer {token}"
# }
#
# # Request Body
# data = {
#     "messageId": "unique-transaction-id-12345",
#     "responseChannelType": "SYNCHRONOUS",
#     "responseChannel": {
#         "responsePayloadFormat": "DEVICEMESSAGE"
#     },
#     "messageType": "application/vnd.elavon.transaction-b.v1+json",
#     "message": {
#         "referenceNumber": "67362762",
#         "identifiers": {
#             "chain": "TSTLA3",
#             "location": "CFGALLERY",
#             "terminal": "TERM1"
#         },
#         "transType": "SALE",
#         "transAmount": "44.00",
#         "taxList": [
#             {
#                 "taxIndicator": "1",
#                 "taxAmount": "0.70"
#             }
#         ],
#         "manuallyEntered": "FALSE",
#         "partialAuthFlag": "1",
#         "uniqueDeviceId": "11223344",
#         "transactionDateTime": "2025-01-25T03:44:24.770Z",
#         "cashierId": "12340110",
#         "userDefinedData": "123456",
#         "compliance": {
#             "uniqueLaneId": "09033243",
#             "customerCode": "00702011"
#         },
#         "industry": {
#             "data": {
#                 "productCode": "1234",
#                 "invoiceNumber": "214748",
#                 "safetyFields": {
#                     "tokenization": {
#                         "typeRequested": "VN"
#                     }
#                 },
#                 "itemList": [
#                     {
#                         "description": "General Merchandise",
#                         "code": "9837574",
#                         "quantity": 1,
#                         "unitPrice": "10.00"
#                     }
#                 ]
#             }
#         }
#     }
# }
#
# # Send POST request
# try:
#     response = requests.post(url, headers=headers, json=data)
#     response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
#     print("Response:", response.json())
# except requests.exceptions.RequestException as e:
#     print("Request failed:", str(e))

import requests
import logging

from odoo import models, api

_logger = logging.getLogger(__name__)


class TransactionManager(models.Model):
    _name = "transaction.manager"
    _description = "Transaction Manager for Elavon API"

    @api.model
    def send_transaction(self):
        """Sends a transaction request and refreshes token if expired."""
        config = self.env['ir.config_parameter'].sudo()
        token = config.get_param('authetication_config')

        if not token:
            # Fetch a new token and optionally store it
            token = self.env["authentication.manager"].get_token()
            config.set_param('authetication_config', token)

        headers = {
            "Content-Type": "application/vnd.elavon.transaction-b.v1+json",
            "Accept-Version": "V2",
            "Authorization": f"Bearer {token}"
        }

        url = "https://uat.pos.hpi.elavonaws.com/devices/XrkYrftYmyXGp2fb/message"

        # Define the transaction payload. Replace or update the values as needed.
        data = {
            "messageId": "unique-transaction-id-12345",
            "responseChannelType": "SYNCHRONOUS",
            "responseChannel": {
                "responsePayloadFormat": "DEVICEMESSAGE"
            },
            "messageType": "application/vnd.elavon.transaction-b.v1+json",
            "message": {
                "referenceNumber": "67362762",
                "identifiers": {
                    "chain": "TSTLA3",
                    "location": "CFGALLERY",
                    "terminal": "TERM1"
                },
                "transType": "SALE",
                "transAmount": "44.00",
                # "taxList": [
                #     {
                #         "taxIndicator": "1",
                #         "taxAmount": "0.70"
                #     }
                # ],
                "manuallyEntered": "FALSE",
                "partialAuthFlag": "1",
                "uniqueDeviceId": "11223344",
                "transactionDateTime": "2025-01-25T03:44:24.770Z",
                "cashierId": "12340110",
                "userDefinedData": "123456",
                "compliance": {
                    "uniqueLaneId": "09033243",
                    "customerCode": "00702011"
                },
                "industry": {
                    "data": {
                        "productCode": "1234",
                        "invoiceNumber": "214748",
                        "safetyFields": {
                            "tokenization": {
                                "typeRequested": "VN"
                            }
                        },
                        "itemList": [
                            {
                                "description": "General Merchandise",
                                "code": "9837574",
                                "quantity": 1,
                                "unitPrice": "10.00"
                            }
                        ]
                    }
                }
            }
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            # Check if the error is due to token expiration (HTTP 401)
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
                    _logger.error("Transaction retry failed: %s", ex)
                    raise ValueError(f"Transaction request failed after token refresh: {ex}")
            else:
                _logger.error("Transaction request failed: %s", e)
                raise ValueError(f"Transaction request failed: {str(e)}")
        except requests.exceptions.RequestException as e:
            _logger.error("Transaction request encountered an error: %s", e)
            raise ValueError(f"Transaction request encountered an error: {str(e)}")


