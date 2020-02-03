from flask import Blueprint, render_template

from app.models import Term, Gloss, StaticContent

main_blueprint = Blueprint('main', __name__, template_folder='templates')

@main_blueprint.route('/')
def home_page():
    term_count = Term.query.outerjoin(Gloss).count()
    text = StaticContent.query.get("home_page").body_html
    return render_template('home_page.html', term_count=term_count, text=text)

@main_blueprint.route('/about')
def about_page():
    term_count = Term.query.outerjoin(Gloss).count()
    text = StaticContent.query.get("about_page").body_html
    return render_template('about_page.html', term_count=term_count, text=text)

