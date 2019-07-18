from flask import Blueprint, flash, render_template, request
from flask_user import current_user

from app import forms

from app.models import Term

main_blueprint = Blueprint('main', __name__, template_folder='templates')

def register_blueprints(app):
    app.register_blueprint(main_blueprint)

@main_blueprint.route('/')
def home_page():
    gloss_count = Gloss.query.count()
    return render_template('home_page.html', gloss_count = gloss_count)

@main_blueprint.route('/search', methods=['GET', 'POST'])
def search_page():
    results = []
    page = request.args.get('page', 1, type=int)
    form = forms.SearchForm(request.form, obj=current_user)
    if form.validate_on_submit():
        flash("{} {}".format(form.concept.data, form.term.data), "primary")
    else:
        results = Term.query.paginate(page, 10, False)

    print(results.items[0].concept.name)
    return render_template('search_page.html', form=form, results=results)
