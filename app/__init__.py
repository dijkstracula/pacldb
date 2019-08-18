import os

from flask import Flask
from flask_user import UserManager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import Config

csrf_protect = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()

from app.models import Concept, Gloss, Language, Term, User

def create_app(config=Config):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config)

    # Setup DB
    db.init_app(app)
    with app.app_context():
        db.create_all()
        migrate.init_app(app, db)

    #CSRF
    csrf_protect.init_app(app)

    # Setup Flask-User to handle user account related forms
    user_manager = UserManager(app, db, models.User)

    from .routes import register_blueprints
    register_blueprints(app)

    @app.context_processor
    def context_processor():
        return dict(user_manager=user_manager)

    return app
