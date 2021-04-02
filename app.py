#!/usr/bin/env python3
import os

from flask import *
from flask_jwt_extended import *

from config import config
from modules.register.register import app_register
from modules.login.login import app_login
from modules.topup.topup import app_topup
from modules.payment.payment import app_payment
from modules.transfer.transfer import app_transfer
from modules.report.report import app_report
from modules.profile.profile import app_profile

#flask setup
app = Flask(__name__)
app.config['SECRET_KEY'] = config.APP_SECRET_KEY
app.config["JWT_SECRET_KEY"] = config.APP_SECRET_KEY
jwt = JWTManager(app)

# register routes from urls
app.register_blueprint(app_register)
app.register_blueprint(app_login)
app.register_blueprint(app_topup)
app.register_blueprint(app_payment)
app.register_blueprint(app_transfer)
app.register_blueprint(app_report)
app.register_blueprint(app_profile)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=60027)