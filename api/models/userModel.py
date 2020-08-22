from pymodm import MongoModel, fields

class User(MongoModel):
    id = fields.CharField(required=True, primary_key=True)
    name = fields.CharField(required=True)
    email = fields.EmailField(required=True)
    password = fields.CharField(required=True)