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

def add_edit(userId):
    user_search_res = userModel.User.objects.raw({'_id': userId})
    if (user_search_res.count() > 0):
        today = datetime.today().strftime('%Y-%m-%d')
        user = user_search_res.first()
        if (today not in user_search_res.editHistory):
            user.editHistory[today] = 0
        user.editHistory[today] += 1
        user.save()

def get_user_profile(userId):
    user_search_res = userModel.User.objects.raw({'_id': userId})
    if (user_search_res.count() == 0):
        return None
    else:
        user_res = user_search_res.first()
        return {
            "id": user_res.id,
            "username": user_res.username,
            "name": user_res.name          
        }        


def get_edit_history(userId, dayCount):
    user_search_res = userModel.User.objects.raw({'_id': userId})
    editHistory = {}
    if (user_search_res.count() > 0):
        user = user_search_res.first()
        curDate = datetime.today()
        for i in range(dayCount):
            dateStr = curDate.strftime('%Y-%m-%d')                        
            if (dateStr in user.editHistory):
                editHistory[dateStr] = user.editHistory[dateStr]
            else:
                editHistory[dateStr] = 0
            curDate = curDate - timedelta(days=1)            
    return editHistory


