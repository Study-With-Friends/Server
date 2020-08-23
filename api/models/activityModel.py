from pymodm import MongoModel, fields
from api.models import userModel
from api.models import fileModel

class Activity(MongoModel):
    id = fields.CharField(required=True, primary_key=True)    
    eventType = fields.CharField(required=True) # event type
    file = fields.ReferenceField(required=True, model=fileModel.File)
    owner = fields.ReferenceField(required=True, model=userModel.User)
    timestamp = fields.DateTimeField(required=True)