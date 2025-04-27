from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret+jdkjdkst'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///databaseN.sqlite3"
    #UPLOAD_FOLDER = 'static'
    #app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix ='/')
    app.register_blueprint(auth,url_prefix ='/')



   





    from .models import User, Song , Playlist, Review,Album
    
    with app.app_context():
        db.create_all()
    
    return app


def create_database(app):
    if not path.exists('website/databaseN.sqlite3'):
        db.create_all(app=app)
        print('Created Database!')



    

    


def create_database(app):
    if not path.exists('website/databaseN.sqlite3'):
        db.create_all(app=app)
        print('Created Database!')