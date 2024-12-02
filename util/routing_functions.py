from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt
import uuid
import hashlib
import json
import html
from bson.json_util import dumps
from flask import request, redirect, make_response
import time


mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]
user_collection = db["users"]
auth_collection = db["auth_tokens"]
post_collection = db["messages"]
reaction_collection = db["reactions"]

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# verifies login credentials macth
# issue auth token
def verify_login():
    username = html.escape(request.form.get('username'))
    password = request.form.get('password')
    user = user_collection.find_one({"username": username})

    if username is None or password is None or user is None:
        return redirect("/?err=passwordsdontmatch", code=302)

    if bcrypt.checkpw(password.encode('utf-8'), user['password']):
        auth_token = str(uuid.uuid4())
        token_hash = hashlib.sha256(auth_token.encode('utf-8')).hexdigest()
        auth_collection.insert_one({
            "username": user['username'],
            "token_hash": token_hash,
            "user_id": user['_id'],
            "token_expire": int(time.time())+3600
        })
        response = make_response(redirect('/'))
        response.set_cookie('auth_token', auth_token, httponly=True, max_age=3600)
        return response
    else:
        return redirect("/?err=passwordsdontmatch", code=302)

# verify password matches requirements
# verify username doesn't already exist
# then add user to user_collection
def verify_pass():
    username = html.escape(request.form.get('username'))
    password = request.form.get('password1')

    min_length = 8
    requires_digit = any(char.isdigit() for char in password)
    requires_upper = any(char.isupper() for char in password)
    requires_lower = any(char.islower() for char in password)
    requires_special = any(char in "!@#$%^&*()-_+=" for char in password)

    if not username or not password:
        return redirect("/")

    if len(password) < min_length:
        return redirect("/?registerError=Password%20must%20be%20at%20least%208%20characters%20long")
    if not requires_digit:
        return redirect("/?registerError=Password%20must%20contain%20at%20least%20one%20digit")
    if not requires_upper:
        return redirect("/?registerError=Password%20must%20contain%20at%20least%20one%20uppercase%20letter")
    if not requires_lower:
        return redirect("/?registerError=Password%20must%20contain%20at%20least%20one%20lowercase%20letter")
    if not requires_special:
        return redirect("/?registerError=Password%20must%20contain%20at%20least%20one%20special%20character")

    if user_collection.find_one({"username": username}):
        return redirect("/?registerError=Username%20already%20exists")

    return None

    

def register_user():
    username = html.escape(request.form.get('username'))
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if password1 != password2:
        return redirect("/?err=regpasswordsdontmatch", code=302)
           
    if user_collection.find_one({"username": username}):
      return redirect("/?err=usernametaken", code=302)
    verification_result = verify_pass()
    
    if verification_result is not None:
        return verification_result

    password_hash = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
    user_collection.insert_one({ 
        "username": username,
        "password": password_hash
    })
    return redirect('/landing')

def validate_auth_token(token):
    if token is None:
        return False
    token_hash = hashlib.sha256(token.encode('utf-8')).hexdigest()
    userWithToken = auth_collection.find_one({"token_hash":token_hash})

    if userWithToken is None:
        return False
    else:
        return int(userWithToken["token_expire"])>int(time.time())
def username_for_auth_token(token):
    token_hash = hashlib.sha256(token.encode('utf-8')).hexdigest()
    userWithToken = auth_collection.find_one({"token_hash":token_hash})
    return userWithToken["username"]
  
# logout user by removing auth token
def logout_user():
    auth_token = request.cookies.get('auth_token')

    if not auth_token:
        return redirect('/')

    token_hash = hashlib.sha256(auth_token.encode('utf-8')).hexdigest()

    auth_collection.delete_one({"token_hash": token_hash})

    response = make_response(redirect('/'))
    response.set_cookie('auth_token', '', httponly=True, expires=0) 

    return response

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_post():
    auth_token = request.cookies.get('auth_token')
    user=username_for_auth_token(auth_token)



    post_collection.insert_one({
        "title":html.escape(request.form.get('title')),
        "description":html.escape(request.form.get('description')),
        "time": int(time.time()),
        "username":user
    })
    return dumps({'success':True}), 200, {'ContentType':'application/json'}

def send_post_history():
    pipeline = [
    {
        '$lookup': {
            'from': 'reactions', 
            'localField': '_id', 
            'foreignField': 'postID', 
            'as': 'reactions'
        }
    }
]
    auth_token = request.cookies.get('auth_token')
    user= "" if auth_token is None else username_for_auth_token(auth_token)
    return dumps([user,post_collection.aggregate(pipeline)]), 200, {'ContentType':'application/json'} 

def likePost():
    auth_token = request.cookies.get('auth_token')
    user=username_for_auth_token(auth_token)
    query={
        "username": user,
        "reaction":"LIKE",
        "postID":ObjectId(request.form.get("postID"))
    }
    alreadyLiked = reaction_collection.find_one(query)

    if alreadyLiked is None:
        reaction_collection.insert_one(query)
    else:
        reaction_collection.delete_many(query)
    return dumps({'success':True}), 200, {'ContentType':'application/json'} 
