# Flask-User settings
USER_APP_NAME = 'Pan-Athapaskan Comparative Lexicon'
USER_EMAIL_SENDER_NAME = 'Nathan Taylor'
USER_EMAIL_SENDER_EMAIL = 'nbtaylor@gmail.com'

SQLALCHEMY_DATABASE_URI = 'sqlite:///pacl.sqlite' # probably shouldn't live here???
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-User settings
USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
USER_ENABLE_CHANGE_USERNAME = False  # Allow users to change their username
USER_ENABLE_CONFIRM_EMAIL = True  # Force users to confirm their email
USER_ENABLE_FORGOT_PASSWORD = True  # Allow users to reset their passwords
USER_ENABLE_EMAIL = True  # Register with Email
USER_ENABLE_REGISTRATION = False  # Allow new users to register
USER_REQUIRE_RETYPE_PASSWORD = True  # Prompt for `retype password` in:
USER_ENABLE_USERNAME = False  # Register and Login with username
#USER_AFTER_LOGIN_ENDPOINT = 'main.'
#USER_AFTER_LOGOUT_ENDPOINT = 'main.home_page'

ADMINS = [
    '"Admin One" <admin1@gmail.com>',
]
