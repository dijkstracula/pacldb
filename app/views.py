from flask import Blueprint, render_template

from app.models import Term, Gloss

main_blueprint = Blueprint('main', __name__, template_folder='templates')

@main_blueprint.route('/')
def home_page():
    term_count = Term.query.outerjoin(Gloss).count()
    return render_template('home_page.html', term_count=term_count)

