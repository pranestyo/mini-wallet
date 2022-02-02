import json
import uuid
import time
from datetime import datetime

from config import config
import helper

mainDB = config.mainDB


def create_user(params):
    resp = {}
    try:
        first_name = params['first_name']
        last_name = params['last_name']
        phone_number = params['phone_number']
        address = params['address']
        pin = params['pin']

        check_register = check_user({"phone_number": phone_number})

        if check_register['message'] == "REGISTERED":
            resp['message'] = "Phone Number already registered"
        elif check_register['message'] == "NOT_REGISTERED":
            customer_xid = uuid.uuid4()
            created_date = int(time.time() * 1000)

            # insert user_account
            insert_user = mainDB.user_account.insert({
                "customer_xid": str(customer_xid),
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": phone_number,
                "address": address,
                "pin": pin,
                "created_date": int(time.time() * 1000)
            })

            # create virtual account
            # create_va = create_virtual_account(str(customer_xid))

            # response result
            result = {
                "customer_xid": str(customer_xid),
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": phone_number,
                "address": address,
                "created_date": helper.timectime(created_date/1000)
            }

            resp['status'] = "SUCCESS"
            resp['result'] = result
        else:
            resp['message'] = "ERROR_IN_CHECK_USER"

        results = json.dumps(resp)
        return json.loads(results)

    except Exception as e:
        print(e)
        resp['message'] = "ERROR_CREATE_USER"
        results = json.dumps(resp)
        return json.loads(results)


def check_user(params):
    resp = {}
    try:
        phone_number = params['phone_number']
        check_user = mainDB.user_account.find_one(
            {"phone_number": phone_number})
        if check_user:
            resp['message'] = "REGISTERED"
        else:
            resp['message'] = "NOT_REGISTERED"

        results = json.dumps(resp)
        return json.loads(results)
    except:
        resp['message'] = "ERROR_CHECK_USER"

        results = json.dumps(resp)
        return json.loads(results)


def create_virtual_account(customer_xid):
    resp = {}
    check_account = mainDB.virtual_account.find_one(
        {"owned_by": customer_xid, "status": "enabled"})
    if check_account:
        resp["message"] = "The account is enabled"

        results = json.dumps(resp)
        return json.loads(results)
    else:
        now = datetime.now()
        today = now.strftime("%Y-%m-%dT%H:%M:%S")
        create_va = mainDB.virtual_account.insert({
            "owned_by": customer_xid,
            "status": "enabled",
            "enabled_at": today,
            "balance": 0
        })

        data = {
            "wallet": {
                "id": str(create_va),
                "owned_by": customer_xid,
                "status": "enabled",
                "enabled_at": today,
                "balance": 0
            }
        }
        resp["status"] = "success"
        resp["data"] = data

        results = json.dumps(resp)
        return json.loads(results)


def get_virtual_account(customer_xid):
    resp = {}
    check_account = mainDB.virtual_account.find_one({"owned_by": customer_xid})

    if check_account:
        data = {
            "wallet": {
                "id": str(check_account["_id"]),
                "owned_by": check_account["owned_by"],
                "status": check_account["status"],
                "enabled_at": check_account["enabled_at"],
                "balance": check_account["balance"]
            }
        }
        resp["status"] = "success"
        resp["data"] = data

        results = json.dumps(resp)
        return json.loads(results)


def deactivate_virtual_account(customer_xid):
    resp = {}
    check_account = mainDB.virtual_account.find_one(
        {"owned_by": customer_xid, "status": "enabled"})
    if check_account:
        update_va = mainDB.virtual_account.update({
            "owned_by": customer_xid
        }, {
            "$set": {"status": "disabled"}
        })
        resp["status"] = "success"
        now = datetime.now()
        today = now.strftime("%Y-%m-%dT%H:%M:%S")
        result = {
            "wallet": {
                "id": str(check_account),
                "owned_by": customer_xid,
                "status": "disabled",
                "disabled_at": today,
                "balance": check_account["balance"]
            }
        }
        resp["data"] = result

        results = json.dumps(resp)
        return json.loads(results)
    else:
        resp["message"] = "Wallet id not found."

        results = json.dumps(resp)
        return json.loads(results)
