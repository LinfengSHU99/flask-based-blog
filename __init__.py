import datetime
import time
from flask import Flask, render_template, session, request, redirect, current_app, g
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, InputRequired
from flask_pagedown import PageDown
from flask_pagedown.fields import PageDownField
import os
from flask_sqlalchemy import SQLAlchemy
from config import Config


db = SQLAlchemy()
bootstrap = Bootstrap()
pagedown = PageDown()


def create_app():
    app = Flask(__name__)
    Config.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    pagedown.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app