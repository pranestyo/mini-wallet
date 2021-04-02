import json
import time
import uuid

# from flask_jwt_extended import *

from config import config
import helper

mainDB = config.mainDB

def payment(params):
    resp = {}
    try:
        amount = params['amount']
        remarks = params['remarks']
        current_user = params['current_user']
        
        payment_id = uuid.uuid4()
        created_date = int(time.time() * 1000)
        check_va = mainDB.virtual_account.find_one({"user_id": current_user})
        balance_before = check_va['balance']
        balance_after = balance_before - amount

        if balance_after < 0:
            resp['message'] = "Balance Not Enough"

            results = json.dumps(resp)
            return json.loads(results)

        create_payment = trx_payment({
            "payment_id": str(payment_id),
            "user_id": current_user,
            "amount": amount,
            "remarks": remarks,
            "balance_before": balance_before,
            "balance_after": balance_after,
            "created_date": created_date
        })

        update_va = mainDB.virtual_account.update({
            "user_id": current_user
        },{
            "$set": {"balance": balance_after}
        })

        result = {
            "payment_id": str(payment_id),
            "amount": amount,
            "remarks": remarks,
            "balance_before": balance_before,
            "balance_after": balance_after,
            "created_date": helper.timectime(created_date/1000)
        }

        resp['status'] = "SUCCESS"
        resp['result'] = result

        results = json.dumps(resp)
        return json.loads(results)

    except Exception as e:
        print(e)
        resp['message'] = "PAYMENT_ERROR"

        results = json.dumps(resp)
        return json.loads(results)

def trx_payment(params):
    insert = mainDB.user_payment.insert({
        "payment_id": params['payment_id'],
        "user_id": params['user_id'],
        "amount": params['amount'],
        "remarks": params['remarks'],
        "balance_before": params['balance_before'],
        "balance_after": params['balance_after'],
        "status": "SUCCESS",
        "transaction_type": "DEBIT",
        "created_date": params['created_date']
    })
