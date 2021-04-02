import json
import time
import uuid

# from flask_jwt_extended import *

from config import config
import helper

mainDB = config.mainDB

def transfer(target_user,amount,remarks,current_user):
    resp = {}
    try:
        transfer_id = uuid.uuid4()
        created_date = int(time.time() * 1000)
        check_va = mainDB.virtual_account.find_one({"user_id": current_user})
        balance_before = check_va['balance']
        balance_after = balance_before - amount

        if balance_after < 0:
            resp['message'] = "Balance Not Enough"

            results = json.dumps(resp)
            return json.loads(results)

        create_transfer = trx_transfer({
            "transfer_id": str(transfer_id),
            "user_id": current_user,
            "amount": amount,
            "remarks": remarks,
            "balance_before": balance_before,
            "balance_after": balance_after,
            "target_user": target_user,
            "created_date": created_date
        })

        update_va = mainDB.virtual_account.update({
            "user_id": current_user
        },{
            "$set": {"balance": balance_after}
        })

        check_va_target = mainDB.virtual_account.find_one({"user_id": target_user})
        update_va_target = mainDB.virtual_account.update({
            "user_id": target_user
        },{
            "$set": {"balance": check_va_target['balance']+amount}
        })

        result = {
            "transfer_id": str(transfer_id),
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

def trx_transfer(params):
    insert = mainDB.user_transfer.insert({
        "transfer_id": params['transfer_id'],
        "user_id": params['user_id'],
        "amount": params['amount'],
        "remarks": params['remarks'],
        "balance_before": params['balance_before'],
        "balance_after": params['balance_after'],
        "target_user": params['target_user'],
        "status": "SUCCESS",
        "transaction_type": "DEBIT",
        "created_date": params['created_date']
    })
