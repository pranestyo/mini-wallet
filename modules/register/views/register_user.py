import json
import uuid
import time

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
            user_id = uuid.uuid4()
            created_date = int(time.time() * 1000)

            #insert user_account
            insert_user = mainDB.user_account.insert({
                "user_id": str(user_id),
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": phone_number,
                "address": address,
                "pin": pin,
                "created_date": int(time.time() * 1000)
            })
            
            #create virtual account
            create_va = create_virtual_account(str(user_id))

            #response result
            result = {
                "user_id": str(user_id),
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
        check_user = mainDB.user_account.find_one({"phone_number": phone_number})
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

def create_virtual_account(user_id):
    create_va = mainDB.virtual_account.insert({
        "user_id": user_id,
        "balance": 0
    })
