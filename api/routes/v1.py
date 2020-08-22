from flask_restx import Namespace, Resource


api = Namespace('v1', description='V1 API')

@api.route('/test')
class Projects(Resource):
     def get(self):
        return "test"