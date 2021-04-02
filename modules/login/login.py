import os
import json

from flask import *

from modules.login.views import auth

#flask setup
app_login = Blueprint('login', __name__,)

@app_login.route('/login', methods=['POST'])
def login():
    params = {}
    params['phone_number'] = request.json.get('phone_number')
    params['pin'] = request.json.get('pin')
    
    result = auth.auth_login(params)
    return jsonify(result)