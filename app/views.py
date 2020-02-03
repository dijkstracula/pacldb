from flask import Blueprint, render_template

from app.models import Term, Gloss, StaticContent, User

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
    sources = Gloss.query.distinct(Gloss.source).order_by(Gloss.source).all()
    sources = [g.source for g in sources if g.source]

    users = User.query.order_by(User.last_name).all()
    users = [(u.first_name, u.last_name) for u in users if u.first_name and u.last_name]
    return render_template('about_page.html', term_count=term_count, text=text, sources=sources, users=users)

