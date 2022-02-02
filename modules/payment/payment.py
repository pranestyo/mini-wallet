import os
import json

from flask import *
from flask_jwt_extended import *

from modules.payment.views import payment

# flask setup
app_payment = Blueprint('payment', __name__,)


@app_payment.route('/api/v1/wallet/withdrawals', methods=['POST'])
@jwt_required()
def payment_trx():
    params = {}
    params['amount'] = request.json.get('amount')
    params['reference_id'] = request.json.get('reference_id')
    params['current_user'] = get_jwt_identity()

    result = payment.payment(params)
    return jsonify(result)
