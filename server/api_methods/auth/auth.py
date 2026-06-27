
import os

import jwt
from datetime import datetime, timedelta

from flask import request, make_response

from db.db import User, db
import bcrypt

def hash_password(password):
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt() # generation of salt (random symbols against the brootforce)
    password_bytes = bcrypt.hashpw(password_bytes, salt)
    return password_bytes.decode("utf-8")

def signup_user():
    try:
        username = request.json["username"] # all the user fields |
        password = request.json["pswrd"]

        # crypting password
        password = hash_password(password)

        date_created = datetime.now()

        # JWT GENERATION />

        payload = {
            "username": username # payload for jwt
        }
        payload["exp"] = datetime.now() + timedelta(hours=2400) # giving big expiration time for refresh token

        SECRET = os.getenv("SECRET_KEY") # jwt secret
        access_token = jwt.encode(payload, SECRET, "HS256")

        user = User(username=username, pswrd=password, create_date=date_created) # user row to add to db

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

def greet():
    return {
        "message": "hello! this is backend for my pet-project"
    }