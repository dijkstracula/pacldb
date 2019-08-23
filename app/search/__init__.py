from flask import Blueprint

search_blueprint = Blueprint('search', __name__, template_folder='../templates', url_prefix='/search')

from . import views
