import os
import json

from flask import *
from flask_jwt_extended import *

from modules.report.views import report

#flask setup
app_report = Blueprint('report', __name__,)

@app_report.route('/transactions', methods=['GET'])
@jwt_required()
def transactions():
    params = {}
    params['user_id'] = get_jwt_identity()
    
    result = report.all_trx(params)
    return jsonify(result)
    