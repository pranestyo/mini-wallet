import json
import uuid
import time

from config import config
import helper

mainDB = config.mainDB

def update(params):
    resp = {}
    try:
        first_name = params['first_name']
        last_name = params['last_name']
        phone_number = params['phone_number']
        address = params['address']
        current_user = params['current_user']

        check_user = mainDB.user_account.find_one({
            "user_id": current_user
        })
        print(check_user)

        if check_user:
            update_date = int(time.time() * 1000)
            update = mainDB.user_account.update({
                "user_id": current_user
            },{
                "$set": {
                        "address": address,
                        "update_date": update_date
                    }
            })

            result = {
                "user_id": current_user,
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": phone_number,
                "address": address,
                "update_date": helper.timectime(update_date/1000)
            }

            resp['status'] = "SUCCESS"
            resp['result'] = result
        else:
            resp['message'] = "ERROR_CHECK_USER_IN_UPDATE"
        
        results = json.dumps(resp)
        return json.loads(results)

    except Exception as e:
        print(e)
        resp['message'] = "ERROR_UPDATE_PROFILE"
        results = json.dumps(resp)
        return json.loads(results)
