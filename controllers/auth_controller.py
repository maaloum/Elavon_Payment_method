from odoo import http
from odoo.http import request, Response
import json

class AuthController(http.Controller):

    @http.route('/api/login', type='json', auth="public", methods=['POST'])
    def login(self, **post):
        username = post.get("username")
        password = post.get("password")

        if not username or not password:
            return {"status": "error", "message": "Missing username or password"}

        conf_model = request.env["authentication.conf"]
        response = conf_model.authenticate_user({"username": username, "password": password})

        return response
