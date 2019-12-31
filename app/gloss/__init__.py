from flask import Blueprint

gloss_blueprint = Blueprint('gloss', __name__, template_folder='../templates', url_prefix='/gloss')

from . import views

