from flask_restx import Namespace, Resource, reqparse
import flask_login
from api.controllers import userController
from datetime import datetime, timedelta

api = Namespace('v1', description='V1 API')

@api.route('/user')
class User(Resource):
    @flask_login.login_required
    def get(self):        
        return flask_login.current_user.data

@api.route('/curuser/register')
class CurUserRegister(Resource):
    def post(self):
         parser = reqparse.RequestParser()
         parser.add_argument('name', type=str, required=True)
         parser.add_argument('email', type=str, required=True)
         parser.add_argument('password', type=str, required=True)
         return userController.register_user(**parser.parse_args())


@api.route('/curuser/login')
class CurUserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        user_res = userController.validate_user(**parser.parse_args())
        if (user_res[0]):
            flask_login.login_user(user_res[0],
                                   remember=True,
                                   duration=timedelta(days=30))
        return user_res[1]

@api.route('/curuser/logout')
class CurUserLogout(Resource):
    @flask_login.login_required
    def post(self):
        flask_login.logout_user()
        return True
