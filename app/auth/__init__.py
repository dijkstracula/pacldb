from flask import Blueprint

auth_blueprint = Blueprint('auth', __name__, template_folder='../templates', url_prefix='/auth')

from . import views
