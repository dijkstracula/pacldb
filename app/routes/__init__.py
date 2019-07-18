from flask import Blueprint, flash, render_template, request
from flask_user import current_user

from app import forms

main_blueprint = Blueprint('main', __name__, template_folder='templates')

def register_blueprints(app):
    app.register_blueprint(main_blueprint)

@main_blueprint.route('/')
def home_page():
    return render_template('home_page.html')

@main_blueprint.route('/search', methods=['GET', 'POST'])
def search_page():
    form = forms.SearchForm(request.form, obj=current_user)
    if form.validate_on_submit():
        flash("{} {}".format(form.concept.data, form.term.data), "primary")

    return render_template('search_page.html', form=form)
