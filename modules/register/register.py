import os
import json

from flask import *

from modules.register.views import register_user

#flask setup
app_register = Blueprint('register', __name__,)

@app_register.route('/register', methods=['POST'])
def register():
    params = {}
    params['first_name'] = request.json.get('first_name')
    params['last_name'] = request.json.get('last_name')
    params['phone_number'] = request.json.get('phone_number')
    params['address'] = request.json.get('address')
    params['pin'] = request.json.get('pin')
    
    result = register_user.create_user(params)
    return jsonify(result)