from api.controllers import fileController, activityController
import flask_login
import shortuuid
from werkzeug.security import generate_password_hash, check_password_hash
from api.models import userModel, activityModel, fileModel
from api.utils.api import makeSerializable
from datetime import datetime, timedelta
from random import randint
import pymongo

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

def get_user(user):
    user = _get_user(user.id)
    if not user:
        return None
    return makeSerializable(user.to_son().to_dict())

def register_user(name, username, password, school, location):
    user_search_res = userModel.User.objects.raw({'username': username})
    if (user_search_res.count() != 0):
        return "A user with that username already exists.", 400
    user_id = shortuuid.uuid()
    user = userModel.User(
        id=user_id,
        avatar="/pf/" + str(randint(1, 100)) + ".jpg",
        name=name,
        username=username,
        password=generate_password_hash(password),
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
        if (check_password_hash(user_res.password, password)):
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
    edits_for_file = {}
    lower_time_bound = datetime.today() - timedelta(days=dayCount)
    activities_search_res = activityModel.Activity.objects.raw({'timestamp' : {'$gte': lower_time_bound }}).aggregate({'$sort': {'timestamp': pymongo.DESCENDING}})

    owner_cache = {}
    file_cache = {}
        
    query_set = list(activities_search_res)
    for activity in query_set:
        start_time = datetime.now().timestamp()
        formatted = activity['timestamp'].strftime('%Y-%m-%d')

        if formatted not in activities:
            activities[formatted] = []

        new_activity = makeSerializable(activity)

        if (new_activity['owner'] not in owner_cache):
            owner_cache[new_activity['owner']] = makeSerializable(userModel.User.objects.raw({'_id': new_activity['owner']}).first().to_son().to_dict())
        
        owner = owner_cache[new_activity['owner']]
        new_activity['owner'] = owner

        if (new_activity['file'] not in file_cache):
            file_cache[new_activity['file']] = makeSerializable(fileModel.File.objects.raw({'_id': new_activity['file']}).first().to_son().to_dict())

        file = file_cache[new_activity['file']]
        new_activity['file'] = file

        if file['name'] not in edits_for_file:
            activities[formatted].append(new_activity)
            edits_for_file[file['name']] = {}
            curDate = datetime.today()
            for i in range(dayCount):
                dateStr = curDate.strftime('%Y-%m-%d')
                edits_for_file[file['name']][dateStr] = 0
                curDate = curDate - timedelta(days=1)
        if formatted in edits_for_file[file['name']]:
            edits_for_file[file['name']][formatted] += 1

    return {"activities": activities, "edits_for_file": edits_for_file}

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