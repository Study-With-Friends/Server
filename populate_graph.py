from pymodm.connection import connect
import random
import credentials
import shortuuid
from api.models import activityModel
from datetime import datetime
import math

connect(credentials.dbUrl)

NUM_EVENTS = 1000

USER_ID = 'BdLupoxCurphScQWrmgwev'
FILE_ID = 'H3bmEkCqDjpGebk6kWd4en'

END_TIME = math.floor(datetime.utcnow().timestamp())
START_TIME = END_TIME - (60 * 60 * 24 * 30)

for i in range(NUM_EVENTS):
    activity_id = shortuuid.uuid()

    fake_event_time = datetime.fromtimestamp(random.randint(START_TIME, END_TIME))

    activity = activityModel.Activity(
        id=activity_id,
        eventType='modified',
        file=FILE_ID,
        owner=USER_ID,
        timestamp=fake_event_time
    ).save()
    print(i)