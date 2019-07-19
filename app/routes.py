from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_user import current_user

from sqlalchemy import asc, func

from app import forms
from app.models import Concept, Gloss, Language, Term

from collections import defaultdict

main_blueprint = Blueprint('main', __name__, template_folder='templates')

def register_blueprints(app):
    app.register_blueprint(main_blueprint)

@main_blueprint.route('/')
def home_page():
    gloss_count = Gloss.query.count()
    return render_template('home_page.html', gloss_count = gloss_count)

@main_blueprint.route('/search', methods=['GET', 'POST'])
def search_page():
    page = request.args.get('page', 1, type=int)
    form = forms.SearchForm(request.form, obj=current_user)

    query = Term.query.join(Concept).join(Language).join(Gloss).order_by(asc(func.lower(Concept.name)))

    kwargs = {}

    if form.validate_on_submit():
        kwargs['concept_query'] = form.concept.data
        kwargs['term_query'] = form.term.data
        kwargs['gloss_query'] = form.gloss.data
        return redirect(url_for('main.search_page', **kwargs))
    else:
        form.concept.data = kwargs['concept_query'] = request.args.get('concept_query') or ""
        form.concept.term = kwargs['term_query'] = request.args.get('term_query') or ""
        form.concept.gloss = kwargs['gloss_query'] = request.args.get('gloss_query') or ""


    if kwargs['concept_query']:
        query = query.filter(Concept.name.like(kwargs['concept_query'].strip()))
    if kwargs['term_query'] != "":
        query = query.filter(Term.text.like(kwargs['term_query'].strip()))
    if kwargs['gloss_query']:
        query = query.filter(Gloss.gloss.like(kwargs['gloss_query'].strip()))

    results = query.paginate(page, 25, False)

    begin_cnt = (1 + (25 * (page-1)))
    end_cnt = min(query.count(), (25 * page))
    flash("{} to {} of {} (page {} of {})".format(begin_cnt, end_cnt, query.count(), results.page, results.pages), "primary")

    kwargs['next_url'] = url_for('main.search_page', page=results.next_num, **kwargs) \
        if results.has_next else None
    kwargs['prev_url'] = url_for('main.search_page', page=results.prev_num, **kwargs) \
        if results.has_prev else None

    return render_template('search_page.html', form=form, results=results, **kwargs)
