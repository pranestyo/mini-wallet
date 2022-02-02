import os
import json

from flask import *

from modules.login.views import auth

# flask setup
app_login = Blueprint('login', __name__,)


@app_login.route('/api/v1/init', methods=['POST'])
def login():
    params = request.get_json()
    result = auth.auth_login(params)
    return jsonify(result)
