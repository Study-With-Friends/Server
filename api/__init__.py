from flask import Flask
from flask_restx import Resource, Api
from logzero import logger
import credentials
from api.routes import api
from pymodm.connection import connect
from api.controllers import userController
from flask_cors import CORS


def connectWithRetry():
    logger.info('Starting MongoDB Client')
    connect(credentials.dbUrl)
    logger.info('Connected to MongoDB!')


connectWithRetry()

app = Flask(__name__)
app.secret_key = b'\xa3\xd527\xbdq\x8emv\xb2\xca\xb3,\x81\x1f\xc9'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

CORS(app,
     resources={
         r'/*': {
             'origins': [                
                 'http://localhost:3000',
             ]
         }
     },
     supports_credentials=True)

api.init_app(app)

userController.login_manager.init_app(app)
print("Started Flask App")
