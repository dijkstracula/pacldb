import os

from flask import Flask
from flask_pagedown import PageDown
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import Config

csrf_protect = CSRFProtect()
db = SQLAlchemy(engine_options={"pool_pre_ping":True, "pool_recycle":1200})
migrate = Migrate()
login_manager = LoginManager()
pagedown = PageDown()

from app.models import Gloss, Language, Term, User

def create_app(config=Config):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    db.init_app(app)
    with app.app_context():
        db.create_all()
        migrate.init_app(app, db)

    csrf_protect.init_app(app)

    pagedown.init_app(app)

    from .views import main_blueprint
    app.register_blueprint(main_blueprint)

    from .browse import browse_blueprint
    app.register_blueprint(browse_blueprint)

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .lexicon import lexicon_blueprint
    app.register_blueprint(lexicon_blueprint)

    from .gloss import gloss_blueprint
    app.register_blueprint(gloss_blueprint)

    from .admin import admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app
