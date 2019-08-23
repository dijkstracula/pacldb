from flask import Blueprint, render_template

from app.models import Concept

main_blueprint = Blueprint('main', __name__, template_folder='templates')

@main_blueprint.route('/')
def home_page():
    concept_count = Concept.query.count()
    return render_template('home_page.html', concept_count = concept_count)

