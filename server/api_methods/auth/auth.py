
import os

import jwt
from datetime import datetime, timedelta

from flask import request, make_response

from db.db import User, db
import bcrypt

from utils.errors import WrongPasswordException

def hash_password(password):
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt() # generation of salt (random symbols against the brootforce)
    password_bytes = bcrypt.hashpw(password_bytes, salt)
    return password_bytes.decode("utf-8")

def password_correct(ps, ps_from_db):
    pswrd_bytes = ps.encode("utf-8") # bytes of user enterted password
    hashed_pswrd_bytes = ps_from_db.encode("utf-8") # bytes of hash in db

    pswrds_match =  bcrypt.checkpw(pswrd_bytes, hashed_pswrd_bytes) # checks the match

    return pswrds_match

def generate_jwt(payload):
    # JWT GENERATION />
    payload["exp"] = datetime.now() + timedelta(hours=2400) # giving big expiration time for refresh token
    SECRET = os.getenv("SECRET_KEY") # jwt secret
    access_token = jwt.encode(payload, SECRET, "HS256")
    return access_token

def signup_user():
    try:
        username = request.json["username"] # all the user fields |
        password = request.json["pswrd"]

        # crypting password
        password = hash_password(password)

        date_created = datetime.now()

        
        user = User(username=username, pswrd=password, create_date=date_created) # user row to add to db

        # JWT GENERATION />
        payload = {
            "user_id": user.user_id,
            "username": username # payload for jwt
        }
        access_token = generate_jwt(payload)

        db.session.add(user) # adding and committing to db
        db.session.commit()
        

        response_body = {
            "access_token": access_token,
            "status": "success",
            "message": "created successfully"
        }

        return make_response(response_body, 201)
    
    except BaseException as e: # all the user and server errors handling |
        error_response = {}
        status_code = None

        if "psycopg2.errors.UniqueViolation" in e.args[0]: # user already exists error
            error_response = {
                "status": "fail",
                "message": f"user with name '{request.json["username"]}' already exists"
            }
            status_code = 400

        return make_response(error_response, status_code)
    
def signin_user():
    try:
        username = request.json["username"]
        password = request.json["pswrd"]

        user = User.query.filter_by(username=username).one_or_404()

        if not password_correct(password, user.pswrd): # checks if entered password is correct like in db
            raise WrongPasswordException("wrong password")
        

        payload = {
            "user_id": user.user_id,
            "username": username # payload for jwt
        }
        access_token = generate_jwt(payload)

        response_body = {
            "access_token": access_token,
            "status": "success",
            "message": "signin successfully"
        }

        return make_response(response_body, 200)

    except BaseException as e:
        error_response = {"error": str(e)}
        status_code = None
        e = str(e)

        if "404 Not Found" in e: # user already exists error
            error_response = {
                "status": "fail",
                "message": f"user with name '{request.json["username"]}' does not exist"
            }
            status_code = 404
        elif "wrong password" in e:
            error_response = {
                "status": "fail",
                "message": f"your password is wrong"
            }
            status_code = 400

        return make_response(error_response, status_code)
    
def greet():
    return {
        "message": "hello! this is backend for my pet-project"
    }