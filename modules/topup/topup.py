import os
import json

from flask import *
from flask_jwt_extended import *

from modules.topup.views import topup

#flask setup
app_topup = Blueprint('topup', __name__,)

@app_topup.route('/topup', methods=['POST'])
@jwt_required()
def topup_trx():
    params = {}
    params['amount'] = request.json.get('amount')
    params['current_user'] = get_jwt_identity()
    
    result = topup.topup(params)
    return jsonify(result)
    