import os

MONGO_URI = os.environ.get('MONGO_URI')
dbUrl = MONGO_URI if MONGO_URI else "mongodb+srv://user:BHzvOvtAvKzcaA2N@cluster0.kvxb8.mongodb.net/test?retryWrites=true&w=majority"

UPLOAD_FOLDER = "./files"