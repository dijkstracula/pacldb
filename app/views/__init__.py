from flask import Blueprint, render_template
from flask_user import current_user

main_blueprint = Blueprint('main', __name__, template_folder='templates')

def register_blueprints(app):
    app.register_blueprint(main_blueprint)

@main_blueprint.route('/')
def home_page():
    return render_template('home_page.html')
