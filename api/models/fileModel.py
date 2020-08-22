from pymodm import MongoModel, fields
from api.models import userModel

class File(MongoModel):
    id = fields.CharField(required=True, primary_key=True)    
    displayName = fields.CharField(required=True, default='Untitled')
    name = fields.CharField(required=True)
    owner = fields.ReferenceField(required=True, model=userModel.User)
    lastModified = fields.DateTimeField(required=True)