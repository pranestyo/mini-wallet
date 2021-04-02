import json
import time
import uuid

# from flask_jwt_extended import *

from config import config
import helper

mainDB = config.mainDB

def all_trx(params):
    resp = {}
    try:
        user_id = params['user_id']

        get_topup = trx_topup(user_id)
        get_payment = trx_payment(user_id)
        get_transfer = trx_transfer(user_id)
        results = get_topup+get_payment+get_transfer
        resp['status'] = "SUCCESS"
        resp['result'] = results

        results = json.dumps(resp)
        return json.loads(results)
    
    except Exception as e:
        print(e)
        resp['message'] = "GET_REPORT_ERROR"

        results = json.dumps(resp)
        return json.loads(results)

def trx_topup(user_id):
    results = []
    trx_topups = mainDB.user_topup.find({"user_id": user_id})
    for topup in trx_topups:
        data_topup = {
            "top_up_id": topup['top_up_id'],
            "status": topup['status'],
            "user_id": user_id,
            "transaction_type": topup['transaction_type'],
            "amount": topup['amount_top_up'],
            "remarks": "",
            "balance_before": topup['balance_before'],
            "balance_after": topup['balance_after'],
            "created_date": helper.timectime(topup['created_date']/1000)
        }
        results.append(data_topup)

    return results

def trx_payment(user_id):
    results = []
    trx_payments = mainDB.user_payment.find({"user_id": user_id})
    for pay in trx_payments:
        data_pay = {
            "payment_id": pay['payment_id'],
            "status": pay['status'],
            "user_id": user_id,
            "transaction_type": pay['transaction_type'],
            "amount": pay['amount'],
            "remarks": pay['remarks'],
            "balance_before": pay['balance_before'],
            "balance_after": pay['balance_after'],
            "created_date": helper.timectime(pay['created_date']/1000)
        }
        results.append(data_pay)

    return results

def trx_transfer(user_id):
    results = []
    trx_transfers = mainDB.user_transfer.find({"user_id": user_id})
    for transfer in trx_transfers:
        data_transfer = {
            "transfer_id": transfer['transfer_id'],
            "status": transfer['status'],
            "user_id": user_id,
            "transaction_type": transfer['transaction_type'],
            "amount": transfer['amount'],
            "remarks": transfer['remarks'],
            "balance_before": transfer['balance_before'],
            "balance_after": transfer['balance_after'],
            "created_date": helper.timectime(transfer['created_date']/1000)
        }
        results.append(data_transfer)

    return results
