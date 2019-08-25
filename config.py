import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY= os.environ.get('SECRET_KEY') or 'dev'

    # Flask-User settings
    USER_APP_NAME = 'Pan-Dene Comparative Lexicon'
    USER_EMAIL_SENDER_NAME = 'Nathan Taylor'
    USER_EMAIL_SENDER_EMAIL = 'nbtaylor@gmail.com'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgres://localhost/pacl'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    MAIL_SUBJECT_PREFIX = '[Pan-DLC]: '
    MAIL_SENDER = 'Pan-DLC Admin <admin@pan-dlc.herokuapp.com>'

    ADMINS = [
        '"Nathan Taylor" <nbtaylor@gmail.com>',
    ]
