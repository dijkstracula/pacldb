from flask import Blueprint

admin_blueprint = Blueprint('admin', __name__, template_folder='../templates', url_prefix='/admin')

from . import views

