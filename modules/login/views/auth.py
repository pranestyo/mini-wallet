import json

from flask_jwt_extended import *

from config import config

mainDB = config.mainDB

def auth_login(params):
    resp = {}
    try:
        phone_number = params['phone_number']
        pin = params['pin']

        check_user = mainDB.user_account.find_one({
            "phone_number": phone_number,
            "pin": pin
        })

        if check_user:
            #generate token
            user_id = check_user['user_id']
            access_token = create_access_token(identity=user_id, fresh=True)
            refresh_token = create_refresh_token(user_id)
            
            #save token
            check_token = mainDB.user_token.find_one({"user_id": user_id})
            if check_token:
                update_token = update_token_user({
                    "user_id": user_id,
                    "access_token": access_token,
                    "refresh_token": refresh_token
                })
            else:
                save_token = save_token_user({
                    "user_id": user_id,
                    "access_token": access_token,
                    "refresh_token": refresh_token
                })
            
            #response
            result = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
            resp['status'] = "SUCCESS"
            resp['result'] = result
        else:
            resp['message'] = "Phone number and pin doesn’t match."

        results = json.dumps(resp)
        return json.loads(results)

    except Exception as e:
        print(e)
        resp['message'] = "AUTH_LOGIN_ERROR"
        results = json.dumps(resp)

        return json.loads(results)

def save_token_user(params):
    insert = mainDB.user_token.insert({
        "user_id": params["user_id"],
        "access_token": params["access_token"],
        "refresh_token": params["refresh_token"]
    })

def update_token_user(params):
    update = mainDB.user_token.update({
        "user_id": params["user_id"]
    },{
        "$set": {
            "access_token": params["access_token"],
            "refresh_token": params["refresh_token"]
        }
    })

