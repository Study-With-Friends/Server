from api.controllers import userController
from datetime import datetime
import os
import shortuuid
from werkzeug.utils import secure_filename
from credentials import UPLOAD_FOLDER
from api.models import fileModel
from api.utils.api import makeSerializable

def upload_file(user, fileId, fileObj):
    displayName = secure_filename(fileObj.filename)
    fileName = user['id'] + '-' + fileId
    file_search_res = fileModel.File.objects.raw({'name': fileName})
    if (file_search_res.count() == 0):
        file = fileModel.File(
            id=shortuuid.uuid(),
            name=fileName,
            owner=user['id'],
            lastModified=datetime.now(),
            displayName=displayName
        ).save()
    else:
        file = file_search_res.first()
        file.lastModified = datetime.now()
        file.save()
    userController.add_edit(user['id'])
    file_res = makeSerializable(file_search_res.first().to_son().to_dict())
    fileObj.save(os.path.join(UPLOAD_FOLDER, fileName))
    return file_res

def get_user_file_list(userId):
    file_search_res = fileModel.File.objects.raw({'owner': userId})
    query_set = list(file_search_res)
    file_list = []
    for file in query_set:
        file_list.append({
            "displayName": file.displayName,
            "name": file.name
        })
    return file_list

def get_file(fileName):
    try:
        file_str = open(os.path.join(UPLOAD_FOLDER, fileName), 'r').read()
        return file_str
    except Exception:
        return None