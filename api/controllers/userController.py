import flask_login
import shortuuid
from api.models import userModel
from api.utils.api import makeSerializable

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
            "email": user_res.email,
            "name": user_res.name          
        }
        return user

def register_user(name, email, password):
    user_search_res = userModel.User.objects.raw({'email': email})
    if (user_search_res.count() != 0):
        return "A user with that email already exists.", 400
    user_id = shortuuid.uuid()
    print(name)
    print(email)
    print(password)
    user = userModel.User(
        id=user_id,
        name=name,
        email=email,
        password=password
    ).save()
    user_obj = makeSerializable(user.to_son().to_dict())
    return user_obj

def validate_user(email, password):
    if (email is None or password is None):
        return None, None
    user_search_res = userModel.User.objects.raw({'email': email})
    if (user_search_res.count() == 0):
        return None, None
    else:
        user_res = user_search_res.first()
        if (password == user_res.password):
            user = Flask_User()
            user.id = user_res.id          
            return user, makeSerializable(user_res.to_son().to_dict())
        return None, None
