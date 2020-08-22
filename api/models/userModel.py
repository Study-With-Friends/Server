from pymodm import MongoModel, fields

class User(MongoModel):
    id = fields.CharField(required=True, primary_key=True)
    name = fields.CharField(required=True)
    username = fields.UsernameField(required=True)
    password = fields.CharField(required=True)