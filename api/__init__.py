from flask import Flask
from flask_restx import Resource, Api
from logzero import logger
import credentials
from api.routes import api
from pymodm.connection import connect
from api.controllers import userController

def connectWithRetry():
    logger.info('Starting MongoDB Client')
    connect(credentials.dbUrl)
    logger.info('Connected to MongoDB!')


connectWithRetry()

app = Flask(__name__)
app.secret_key = b'\xa3\xd527\xbdq\x8emv\xb2\xca\xb3,\x81\x1f\xc9'

api.init_app(app)

userController.login_manager.init_app(app)
print("Started Flask App")
