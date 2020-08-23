from api.controllers import userController
from datetime import datetime
import os
import shortuuid
from api.models import activityModel
from api.utils.api import makeSerializable

def new_activity(user, eventType, file):

    user_doc = userController._get_user(user)
    if not user_doc:
        return None

    activity_id = shortuuid.uuid()
    activity = activityModel.Activity(
        id=activity_id,
        eventType=eventType,
        file=file,
        owner=user_doc,
        timestamp=datetime.utcnow()
    ).save()

    activity_obj = makeSerializable(activity.to_son().to_dict())
    return activity_obj