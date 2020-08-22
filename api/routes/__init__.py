from flask_restx import Api,Resource

from .v1 import api as ns1

api = Api(title='Study With Friends API', version='1.0', description='API for Study with Friends')

api.add_namespace(ns1)
