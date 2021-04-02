import pymongo
from pymongo import MongoClient

connect = MongoClient('localhost:27017',
                    username='groot',
                    password='qqweasd123$$',
                    authSource='admin',
                    authMechanism='SCRAM-SHA-1')