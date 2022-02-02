from config.database import connect

APP_HOST = "0.0.0.0"
APP_PORT = 8043

APP_SECRET_KEY = "qwertyuvgb897654%&&$$$oprtgfs1245lkhg"
APP_JWT_HEADER_TYPE = "Token"


mainDB = connect.mini_wallet
