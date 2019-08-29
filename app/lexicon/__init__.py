from flask import Blueprint

lexicon_blueprint = Blueprint('lexicon', __name__, template_folder='../templates', url_prefix='/lexicon')

from . import views

