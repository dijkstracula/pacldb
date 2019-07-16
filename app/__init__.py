import os

from flask import Flask
from flask_user import UserManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.config.from_object('app.local_settings')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Setup DB
    #db.create_all()

    # Setup Flask-User to handle user account related forms
    from .models.user_models import User

    user_manager = UserManager(app, db, User)


    from .views import register_blueprints
    register_blueprints(app)

    @app.context_processor
    def context_processor():
        return dict(user_manager=user_manager)

    return app
