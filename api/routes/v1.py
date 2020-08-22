from api.controllers import fileController
from flask_restx import Namespace, Resource, reqparse
import flask_login
from api.controllers import userController
from datetime import datetime, timedelta
from werkzeug.datastructures import FileStorage

api = Namespace('v1', description='V1 API')

@api.route('/curuser')
class User(Resource):
    @flask_login.login_required
    def get(self):        
        return flask_login.current_user.data

@api.route('/curuser/register')
class CurUserRegister(Resource):
    def post(self):
         parser = reqparse.RequestParser()
         parser.add_argument('name', type=str, required=True)
         parser.add_argument('username', type=str, required=True)
         parser.add_argument('password', type=str, required=True)
         return userController.register_user(**parser.parse_args())


@api.route('/curuser/login')
class CurUserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        user_res = userController.validate_user(**parser.parse_args())
        if (user_res[0]):
            flask_login.login_user(user_res[0],
                                   remember=True,
                                   duration=timedelta(days=30))
        else:
            return "Invalid username or password", 403
        return user_res[1], 200

@api.route('/curuser/logout')
class CurUserLogout(Resource):
    @flask_login.login_required
    def post(self):
        flask_login.logout_user()
        return True

@api.route('/user/profile')
class CurUserLogout(Resource):
    @flask_login.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', type=str, required=True)
        return userController.get_user_profile(**parser.parse_args())


@api.route('/user/history')
class CurUserLogout(Resource):
    @flask_login.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', type=str, required=True)
        parser.add_argument('dayCount', type=int, required=True)        
        return userController.get_edit_history(**parser.parse_args())

@api.route('/users')
class AllUsers(Resource):
    @flask_login.login_required
    def get(self):
        parser = reqparse.RequestParser()
        return userController.get_all_users(**parser.parse_args())

@api.route('/files/upload')
class FileUpload(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('fileId', type=str, required=True)
        parser.add_argument('file', location='files', type=FileStorage, required=True)
        args = parser.parse_args()
        print(args['username'])
        print(args['password'])
        user_res = userController.validate_user(args['username'], args['password'])
        if (user_res[0] is None):
            return "Wrong login.", 403

        uploaded_file = args['file']
        fileController.upload_file(user_res[1], args['fileId'], uploaded_file)
        return user_res[1]

@api.route('/files/get')
class FileUpload(Resource):
    @flask_login.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fileName', type=str, required=True)        
        return fileController.get_file(**parser.parse_args())

@api.route('/files/list')
class FileUpload(Resource):
    @flask_login.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', type=str, required=True)        
        return fileController.get_user_file_list(**parser.parse_args())