from api.controllers import fileController
import flask_login
import shortuuid
from api.models import userModel
from api.utils.api import makeSerializable
from datetime import datetime, timedelta

login_manager = flask_login.LoginManager()

class Flask_User(flask_login.UserMixin):
    id = None

@login_manager.user_loader
def user_loader(user_id):
    user_search_res = userModel.User.objects.raw({'_id': user_id})
    if (user_search_res.count() == 0):
        return None
    else:
        user_res = user_search_res.first()
        user = Flask_User()
        user.id = user_res.id
        user.data = {
            "id": user_res.id,
            "username": user_res.username,
            "name": user_res.name          
        }
        return user

def register_user(name, username, password):
    user_search_res = userModel.User.objects.raw({'username': username})
    if (user_search_res.count() != 0):
        return "A user with that username already exists.", 400
    user_id = shortuuid.uuid()
    user = userModel.User(
        id=user_id,
        name=name,
        username=username,
        password=password,
        editHistory={}
    ).save()
    user_obj = makeSerializable(user.to_son().to_dict())
    return user_obj

def validate_user(username, password):
    if (username is None or password is None):
        return None, None
    user_search_res = userModel.User.objects.raw({'username': username})
    if (user_search_res.count() == 0):
        return None, None
    else:
        user_res = user_search_res.first()
        if (password == user_res.password):
            user = Flask_User()
            user.id = user_res.id          
            return user, makeSerializable(user_res.to_son().to_dict())
        return None, None

def get_all_users():
    users = []
    users_search_res = userModel.User.objects.raw({})
    query_set = list(users_search_res)
    for user in query_set:
        users.append(makeSerializable(user.to_son().to_dict()))
    return users, 200

def add_edit(userId, fileName):
    user_search_res = userModel.User.objects.raw({'_id': userId})
    if (user_search_res.count() > 0):
        today = datetime.today().strftime('%Y-%m-%d')
        user = user_search_res.first()
        if (today not in user.editHistory):
            user.editHistory[today] = {}
        if (fileName not in user.editHistory[today]):
            user.editHistory[today][fileName] = []
        user.editHistory[today][fileName].append(str(datetime.now()))
        user.save()

def get_user_profile(username):
    user_search_res = userModel.User.objects.raw({'username': username})
    if (user_search_res.count() == 0):
        return None
    else:
        user_res = user_search_res.first()
        return {
            "id": user_res.id,
            "username": user_res.username,
            "name": user_res.name          
        }        

def get_edit_history(username, dayCount):
    user_search_res = userModel.User.objects.raw({'username': username})
    editHistory = {}
    if (user_search_res.count() > 0):
        user = user_search_res.first()
        curDate = datetime.today()
        for i in range(dayCount):
            dateStr = curDate.strftime('%Y-%m-%d')                        
            if (dateStr in user.editHistory):
                totalEdits = 0
                for file in user.editHistory[dateStr]:
                    totalEdits += len(user.editHistory[dateStr][file])
                editHistory[dateStr] = totalEdits
            else:
                editHistory[dateStr] = 0
            curDate = curDate - timedelta(days=1)            
    return editHistory

def get_activity(username, dayCount):
    user_search_res = userModel.User.objects.raw({'username': username} if username else {})
    activity = {}
    if (user_search_res.count() > 0):
        user = user_search_res.first()
        curDate = datetime.today()
        for i in range(dayCount):
            dateStr = curDate.strftime('%Y-%m-%d')                        
            if (dateStr in user.editHistory):
                activity[dateStr] = []
                for file in user.editHistory[dateStr]:
                    fileData = fileController.get_file_data(file)                    
                    activity[dateStr].append({
                        "username": user.username,
                        "fileName": file,
                        "fileDisplayName": fileData['displayName'] if fileData is not None else '',
                        "edits": user.editHistory[dateStr][file],
                        "createdToday": datetime.strptime(fileData['creationDate'], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d') == dateStr if fileData is not None else ''
                    })
            else:
                activity[dateStr] = []
            curDate = curDate - timedelta(days=1)            
    return activity

def follow_user(user, followUsername):
    user_search_res = userModel.User.objects.raw({'username': user.data['username']})
    user_follow_search_res = userModel.User.objects.raw({'username': followUsername})   
    if (user_follow_search_res.count() == 0):
        return "Follow User not found.", 400
    if (user_search_res.count() == 0):
        return "User not found.", 400
    user = user_search_res.first()
    if (user_follow_search_res.first() not in user.followingList):
        user.followingList.append(user_follow_search_res.first().id)
        user.save()
    return makeSerializable(user.to_son().to_dict())

def unfollow_user(user, unfollowUsername):
    user_search_res = userModel.User.objects.raw({'username': user.data['username']})
    user_unfollow_search_res = userModel.User.objects.raw({'username': unfollowUsername})   
    if (user_unfollow_search_res.count() == 0):
        return "Unfollow User not found.", 400
    if (user_search_res.count() == 0):
        return "User not found.", 400
    user = user_search_res.first()
    if (user_unfollow_search_res.first() in user.followingList):
        user.followingList.remove(user_unfollow_search_res.first())
        user.save()
    return makeSerializable(user.to_son().to_dict())