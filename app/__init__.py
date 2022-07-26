from flask import Flask
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate
from flask_moment import Moment

db = SQLAlchemy()
bootstrap = Bootstrap()
pagedown = PageDown()
migrate = Migrate()
moment = Moment()

def create_app():
    from app.database import Tag, Article, Category, Password
    app = Flask(__name__)
    Config.init_app(app)
    db.init_app(app)
    db.app = app
    moment.init_app(app)
    bootstrap.init_app(app)
    pagedown.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    migrate.init_app(app, db)
    return app
