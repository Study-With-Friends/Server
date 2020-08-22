from pymodm import MongoModel, fields

class User(MongoModel):
    pass
class User(MongoModel):
    id = fields.CharField(required=True, primary_key=True)
    name = fields.CharField(required=True)
    password = fields.CharField(required=True)
    editHistory = fields.DictField(required=True, default={}, blank=True)
    username = fields.CharField(required=True)
    school = fields.CharField()
    location = fields.CharField()
    followingList = fields.ListField(field=fields.ReferenceField(model=User))
    followerList = fields.ListField(field=fields.ReferenceField(model=User))