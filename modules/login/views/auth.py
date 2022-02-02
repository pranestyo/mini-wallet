import json

from flask_jwt_extended import *

from config import config

mainDB = config.mainDB


def auth_login(params):
    resp = {}
    try:
        customer_xid = params['customer_xid']

        check_user = mainDB.user_account.find_one({
            "customer_xid": customer_xid,
        })

        if check_user:
            # generate token
            customer_xid = check_user['customer_xid']
            access_token = create_access_token(
                identity=customer_xid, fresh=True)

            # save token
            check_token = mainDB.user_token.find_one(
                {"customer_xid": customer_xid})
            if check_token:
                update_token = update_token_user({
                    "customer_xid": customer_xid,
                    "access_token": access_token
                })
            else:
                save_token = save_token_user({
                    "customer_xid": customer_xid,
                    "access_token": access_token
                })

            # response
            result = {
                "token": access_token
            }
            resp['status'] = "success"
            resp['data'] = result
        else:
            resp['message'] = "Customer ID doesn’t match."

        results = json.dumps(resp)
        return json.loads(results)

    except Exception as e:
        print(e)
        resp['message'] = "AUTH_LOGIN_ERROR"
        results = json.dumps(resp)

        return json.loads(results)


def save_token_user(params):
    insert = mainDB.user_token.insert({
        "customer_xid": params["customer_xid"],
        "access_token": params["access_token"]
    })


def update_token_user(params):
    update = mainDB.user_token.update({
        "customer_xid": params["customer_xid"]
    }, {
        "$set": {
            "access_token": params["access_token"]
        }
    })
