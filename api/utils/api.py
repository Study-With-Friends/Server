import datetime
import simplejson as json

def makeSerializable(obj):
    serialObj = {}
    for k, v in obj.items():        
        if isinstance(v, dict):
            serialObj[k] = makeSerializable(v)
            continue
        if (not k.startswith('_')):
            if (type(v) is datetime.datetime):
                serialObj[k] = str(v)
            elif (k != 'password'):
                serialObj[k] = v
        elif (k == '_id'):
            serialObj['id'] = v
        elif (k == '_cls'):
            serialObj['_cls'] = v
    return serialObj