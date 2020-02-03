from flask import Blueprint

browse_blueprint = Blueprint('browse', __name__, template_folder='../templates', url_prefix='/browse')

from . import views
