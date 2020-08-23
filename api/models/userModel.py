from pymodm import MongoModel, fields

class User(MongoModel):
    pass
class User(MongoModel):
    id = fields.CharField(required=True, primary_key=True)
    avatar = fields.CharField(required=True)
    name = fields.CharField(required=True)
    password = fields.CharField(required=True)
    username = fields.CharField(required=True)
    school = fields.CharField(blank=True)
    location = fields.CharField(blank=True)
    followingList = fields.ListField(field=fields.ReferenceField(model='User'), blank=True, default=[], required=True)
    followerList = fields.ListField(field=fields.ReferenceField(model='User'), blank=True, default=[], required=True)