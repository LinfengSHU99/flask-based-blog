from flask_sqlalchemy import SQLAlchemy
# from app import app
import os

class Database:

    def __init__(self, app) -> None:
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SECRET_KEY'] = '?'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False