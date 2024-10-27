from pymongo import MongoClient
import bcrypt
import uuid
import hashlib
from flask import request, redirect, make_response



mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]
user_collection = db["users"]
auth_collection = db["auth_tokens"]


# verifies login credentials macth
# issue auth token
def verify_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = user_collection.find_one({"username": username})

    if username is None or password is None:
        return "One of the fields is empty", 400

    if bcrypt.checkpw(password.encode('utf-8'), user['password']):
        auth_token = str(uuid.uuid4())
        token_hash = hashlib.sha256(auth_token.encode('utf-8')).hexdigest()
        auth_collection.insert_one({
            "username": user['username'],
            "token_hash": token_hash,
            "user_id": user['_id'],
        })
        response = make_response(redirect('/'))
        response.set_cookie('auth_token', auth_token, httponly=True, max_age=3600)
        return response
    else:
        return "Invalid username/password", 400

# verify password matches requirements
# verify username doesn't already exist
# then add user to user_collection
def verify_pass():
    username = request.form.get('username')
    password = request.form.get('password1')

    min_length = 8
    requires_digit = any(char.isdigit() for char in password)
    requires_upper = any(char.isupper() for char in password)
    requires_lower = any(char.islower() for char in password)
    requires_special = any(char in "!@#$%^&*()-_+=" for char in password)

    if not username or not password:
        return "Username and password cannot be empty", 400

    if len(password) < min_length:
        return "Password must be at least 8 characters long", 400
    if not requires_digit:
        return "Password must contain at least one digit", 400
    if not requires_upper:
        return "Password must contain at least one uppercase letter", 400
    if not requires_lower:
        return "Password must contain at least one lowercase letter", 400
    if not requires_special:
        return "Password must contain at least one special character ", 400

    if user_collection.find_one({"username": username}):
        return "Username already exists", 400

    return None

    

def register_user():
    username = request.form.get('username')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if password1 != password2:
        return "Passwords do not match", 400
           
    if user_collection.find_one({"username": username}):
        return "Username already taken", 400
    
    verification_result = verify_pass()
    if verification_result is not None:
        return verification_result
    
    password_hash = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
    user_collection.insert_one({ 
        "username": username,
        "password": password_hash
    })
    return redirect('/landing')

# logout user by removing auth token
def logout_user():
    auth_token = request.cookies.get('auth_token')

    if not auth_token:
        return "Error finding an Active seasiion to logout", 400
    
    token_hash = hashlib.sha256(auth_token.encode('utf-8')).hexdigest()

    auth_collection.delete_one({"token_hash": token_hash})

    response = make_response(redirect('/login'))
    response.set_cookie('auth_token', '', httponly=True, expires=0) 

    return response

