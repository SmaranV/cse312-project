from pymongo import MongoClient


mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]
user_collection = db["users"]


# verifies login credentials macth
# issue auth token
def verify_login():
    return

# verify password matches requirements
# verify username doesn't already exist
# then add user to user_collection
def register_user():
    return

# logout user by removing auth token
def logout_user():
    return
