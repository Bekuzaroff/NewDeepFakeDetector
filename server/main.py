import os
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS

from db.db import db
from api_methods.auth.auth import greet, signin_user, signup_user # database instance and tables

load_dotenv() # loads all custom env variables

def create_app():
    app = Flask(__name__) # app enter-point

    # ------ Настройка CORS
    CORS(app, 
         origins=["http://127.0.0.1:5173", "http://127.0.0.1:3000"],  # разрешённые фронты
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # разрешённые методы
         allow_headers=["Content-Type", "Authorization"],  # разрешённые заголовки
         supports_credentials=True  # поддержка кук/токенов
    )

    # ------ env variables of database
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME")


    DB_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}" # database fully concatanated URL

    # db settings (db_URL, Secretkey, etc.)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app

app = create_app() # our main object of backend



@app.post("/auth/user/new/") # all the API routes |
def create_user():
    return signup_user()

@app.post("/auth/user/") # all the API routes |
def sign_in():
    return signin_user()

@app.get("/")
def greeting():
    return greet()



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)

    
    


    

