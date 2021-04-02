import os
import json
from multiprocessing.pool import ThreadPool

from flask import *
from flask_jwt_extended import *

from modules.transfer.views import transfer

#flask setup
app_transfer = Blueprint('transfer', __name__,)
pool = ThreadPool(processes=1)

@app_transfer.route('/transfer', methods=['POST'])
@jwt_required()
def transfer_trx():
    current_user = get_jwt_identity()
    target_user = request.json.get('target_user')
    amount = request.json.get('amount')
    remarks = request.json.get('remarks')
    
    #run in background process
    exc_transfer = pool.apply_async(transfer.transfer, (target_user,amount,remarks,current_user,))

    result = exc_transfer.get()
    return jsonify(result)
    