import os
from flask import Flask
from dotenv import load_dotenv

from db.db import db # database instance

load_dotenv() # loads all custom env variables

def create_app():
    app = Flask(__name__) # app enter-point

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



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)

    
    


    

