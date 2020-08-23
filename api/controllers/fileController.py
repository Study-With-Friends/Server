from api.controllers import userController
from datetime import datetime
import os
import shortuuid
from werkzeug.utils import secure_filename
from credentials import UPLOAD_FOLDER
from api.models import fileModel
from api.utils.api import makeSerializable

def upload_file(user, fileId, fileObj, action):
    print(action)
    file_res = None
    if (fileId is None):
        fileId = "__TEST_ID__"
    fileName = user['id'] + '-' + fileId
    if (fileObj is not None or action == 'deleted'):
        displayName = secure_filename(fileObj.filename)        
        file_search_res = fileModel.File.objects.raw({'name': fileName})        
        if (file_search_res.count() == 0 and action != 'deleted'):
            file = fileModel.File(
                id=shortuuid.uuid(),
                name=fileName,
                owner=user['id'],
                lastModified=datetime.now(),
                displayName=displayName,
                creationDate=datetime.now()
            )
            file.save()
        elif (action == 'deleted'):
            file = file_search_res.first()
            file.delete()
        else:
            file = file_search_res.first()
            file.lastModified = datetime.now()
            file.name=fileName,
            file.save()
        
        file_res = makeSerializable(file.to_son().to_dict())
        fileObj.save(os.path.join(UPLOAD_FOLDER, fileName))
    userController.add_edit(user['id'], fileName)
    return file_res

def get_user_file_list(userId):
    file_search_res = fileModel.File.objects.raw({'owner': userId})    
    query_set = list(file_search_res)
    file_list = []
    for file in query_set:
        file_list.append({
            "displayName": file.displayName,
            "name": file.name,
            "lastModified": str(file.lastModified)
        })
    return file_list

def get_file_data(fileName):
    file_search_res = fileModel.File.objects.raw({'name': fileName})
    if (file_search_res.count() == 0):
        return None
    else:
        return makeSerializable(file_search_res.first().to_son().to_dict())

def get_file(fileName):
    try:
        file_str = open(os.path.join(UPLOAD_FOLDER, fileName), 'r').read()
        return file_str
    except Exception:
        return None