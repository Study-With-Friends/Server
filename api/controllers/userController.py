from api.controllers import fileController, activityController
import flask_login
import shortuuid
from api.models import userModel, activityModel, fileModel
from api.utils.api import makeSerializable
from datetime import datetime, timedelta
from random import randint

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

def _get_user(user_id):
    user_search_res = userModel.User.objects.raw(
        {'_id': user_id})
    if (user_search_res.count() == 0):
        return None
    else:
        user = user_search_res.first()
        return user

def _get_file(file_id):
    file_search_res = fileModel.File.objects.raw(
        {'_id': file_id})
    if (file_search_res.count() == 0):
        return None
    else:
        file = file_search_res.first()
        return file

def register_user(name, username, password, school, location):
    user_search_res = userModel.User.objects.raw({'username': username})
    if (user_search_res.count() != 0):
        return "A user with that username already exists.", 400
    user_id = shortuuid.uuid()
    user = userModel.User(
        id=user_id,
        avatar="https://picsum.photos/id/" + str(randint(0, 100)) + "/300/300",
        name=name,
        username=username,
        password=password,
        school=school,
        location=location,
        followingList = [],
        followerList = []
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

def get_user_profile(username):
    user_search_res = userModel.User.objects.raw({'username': username})
    if (user_search_res.count() == 0):
        return None
    else:
        user_res = user_search_res.first()
        following_list = list(map(lambda user: {
            "id": user.id if user else '',
            "username": user.username if user else '',
            "name": user.name if user else ''
        }, user_res.followingList))
        follower_list = list(map(lambda user: {
            "id": user.id if user else '',
            "username": user.username if user else '',
            "name": user.name if user else ''
        }, user_res.followerList))
        return {
            "id": user_res.id,
            "username": user_res.username,
            "name": user_res.name,
            "followingList": following_list,
            "followerList": follower_list,
            "location": user_res.location,
            "school": user_res.school,
            "avatar": user_res.avatar
        }        

def get_edit_history(username, dayCount):
    editHistory = {}
    lower_time_bound = datetime.today() - timedelta(days=dayCount)
    user_search_res = userModel.User.objects.raw({ 'username': username })
    if (user_search_res.count() == 0):
        return editHistory
    
    user_id = user_search_res.first().id

    activities_search_res = activityModel.Activity.objects.raw({'owner': user_id, 'timestamp' : {'$gte': lower_time_bound }})
    query_set = list(activities_search_res)
    for activity in query_set:
        formatted = activity.timestamp.strftime('%Y-%m-%d')
        editHistory[formatted] = editHistory.get(formatted, 0) + 1       
    return editHistory

def get_activity(username, dayCount):
    activities = {}
    lower_time_bound = datetime.today() - timedelta(days=dayCount)
    activities_search_res = activityModel.Activity.objects.raw({'timestamp' : {'$gte': lower_time_bound }})
    query_set = list(activities_search_res)
    for activity in query_set:
        formatted = activity.timestamp.strftime('%Y-%m-%d')
        activities[formatted] = makeSerializable(activity.to_son().to_dict())
    return activities

def follow_user(user, followUsername):
    if (followUsername == user.data['username']):
        return "You cannot follow yourself", 400
    user_search_res = userModel.User.objects.raw({'username': user.data['username']})
    user_follow_search_res = userModel.User.objects.raw({'username': followUsername})   
    if (user_follow_search_res.count() == 0):
        return "Follow User not found.", 400
    if (user_search_res.count() == 0):
        return "User not found.", 400
    user = user_search_res.first()
    user_follow = user_follow_search_res.first()
    if (user_follow not in user.followingList):
        user.followingList.append(user_follow.id)
        user.save()
    if (user not in user_follow.followerList):
        user_follow.followerList.append(user.id)
        user_follow.save()
    return makeSerializable(user.to_son().to_dict())

def unfollow_user(user, unfollowUsername):
    if (unfollowUsername == user.data['username']):
        return "You cannot unfollow yourself", 400
    user_search_res = userModel.User.objects.raw({'username': user.data['username']})
    user_unfollow_search_res = userModel.User.objects.raw({'username': unfollowUsername})   
    if (user_unfollow_search_res.count() == 0):
        return "Unfollow User not found.", 400
    if (user_search_res.count() == 0):
        return "User not found.", 400
    user = user_search_res.first()
    user_unfollow = user_unfollow_search_res.first()
    if (user_unfollow in user.followingList):
        user.followingList.remove(user_unfollow)
        user.save()
    if (user in user_unfollow.followerList):
        user_unfollow.followerList.remove(user)
        user_unfollow.save()
    return makeSerializable(user.to_son().to_dict())