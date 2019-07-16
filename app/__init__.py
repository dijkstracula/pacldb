import os

from flask import Flask
from flask_user import UserManager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


csrf_protect = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()

from app import models

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY= os.environ.get('SECRET_KEY') or 'dev',
        DATABASE=os.path.join(app.instance_path, 'pacldb.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.config.from_object('app.settings')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # Setup DB
    db.init_app(app)
    with app.app_context():
        db.create_all()
        migrate.init_app(app, db)

    #CSRF
    csrf_protect.init_app(app)

    # Setup Flask-User to handle user account related forms
    user_manager = UserManager(app, db, models.User)

    from .views import register_blueprints
    register_blueprints(app)

    @app.context_processor
    def context_processor():
        return dict(user_manager=user_manager)

    return app
