import json
import time
import uuid

from datetime import datetime

from config import config
import helper

mainDB = config.mainDB


def topup(params):
    resp = {}
    try:
        amount = params['amount']
        reference_id = params['reference_id']
        current_user = params['current_user']

        check_reference = mainDB.user_topup.find_one(
            {"reference_id": reference_id})
        if check_reference:
            resp["message"] = "Reference Id must unique."
            results = json.dumps(resp)
            return json.loads(results)

        top_up_id = uuid.uuid4()
        created_date = int(time.time() * 1000)
        check_va = mainDB.virtual_account.find_one({"owned_by": current_user})
        balance_before = check_va['balance']
        balance_after = balance_before + amount

        create_topup = trx_topup({
            "top_up_id": str(top_up_id),
            "user_id": current_user,
            "amount_top_up": amount,
            "balance_before": balance_before,
            "balance_after": balance_after,
            "reference_id": reference_id,
            "created_date": created_date
        })

        update_va = mainDB.virtual_account.update({
            "owned_by": current_user
        }, {
            "$set": {"balance": balance_after}
        })

        now = datetime.now()
        today = now.strftime("%Y-%m-%dT%H:%M:%S")
        result = {
            "deposit": {
                "id": str(create_topup),
                "deposited_by": current_user,
                "status": "success",
                "deposited_at": today,
                "amount": amount,
                "reference_id": reference_id
            }
        }

        resp['status'] = "success"
        resp['data'] = result

        results = json.dumps(resp)
        return json.loads(results)

    except Exception as e:
        print(e)
        resp['message'] = "TOPUP_ERROR"

        results = json.dumps(resp)
        return json.loads(results)


def trx_topup(params):
    insert = mainDB.user_topup.insert({
        "top_up_id": params['top_up_id'],
        "user_id": params['user_id'],
        "amount_top_up": params['amount_top_up'],
        "balance_before": params['balance_before'],
        "balance_after": params['balance_after'],
        "status": "SUCCESS",
        "transaction_type": "CREDIT",
        "created_date": params['created_date'],
        "reference_id": params['reference_id']
    })

    return insert
