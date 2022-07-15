from flask import Flask
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown
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