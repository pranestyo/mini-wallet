import os
import json

from flask import *
from flask_jwt_extended import *

from modules.register.views import register_user

# flask setup
app_register = Blueprint('register', __name__,)


@app_register.route('/register', methods=['POST'])
def register():
    params = request.get_json()
    print(params)
    result = register_user.create_user(params)
    return jsonify(result)


@app_register.route('/api/v1/wallet', methods=['GET', 'POST', 'PATCH'])
@jwt_required()
def active_wallet():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        result = register_user.create_virtual_account(current_user)
        return jsonify(result)
    elif request.method == 'PATCH':
        result = register_user.deactivate_virtual_account(current_user)
        return jsonify(result)
    else:
        result = register_user.get_virtual_account(current_user)
        return jsonify(result)
