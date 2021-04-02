import os
import json

from flask import *
from flask_jwt_extended import *

from modules.profile.views import update_profile

#flask setup
app_profile = Blueprint('profile', __name__,)

@app_profile.route('/profile', methods=['PUT'])
@jwt_required()
def profile():
    params = {}
    params['first_name'] = request.json.get('first_name')
    params['last_name'] = request.json.get('last_name')
    params['phone_number'] = request.json.get('phone_number')
    params['address'] = request.json.get('address')
    params['current_user'] = get_jwt_identity()
    
    result = update_profile.update(params)
    return jsonify(result)