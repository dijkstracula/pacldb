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

    query_state = {}

    if form.validate_on_submit():
        query_state['concept'] = form.concept.data
        query_state['term'] = form.term.data
        query_state['gloss'] = form.gloss.data
        return redirect(url_for('main.search_page', **query_state))
    else:
        form.concept.data = query_state['concept'] = request.args.get('concept') or ""
        form.term.data = query_state['term'] = request.args.get('term') or ""
        form.gloss.data = query_state['gloss'] = request.args.get('gloss') or ""

    if query_state['concept'] != "":
        query = query.filter(Concept.name.like(query_state['concept'].strip()))
    if query_state['term'] != "":
        query = query.filter(Term.text.like(query_state['term'].strip()))
    if query_state['gloss'] != "":
        query = query.filter(Gloss.gloss.like(query_state['gloss'].strip()))

    results = query.paginate(page, 25, False)

    pagination_state = {}
    pagination_state["next_url"] = url_for('main.search_page',
            page=results.next_num,
            **query_state) \
        if results.has_next else None
    pagination_state["prev_url"] = url_for('main.search_page',
            page=results.prev_num,
            **query_state) \
        if results.has_prev else None

    pagination_state['total_cnt'] = query.count()

    pagination_state['begin_cnt'] = (1 + (25 * (page-1)))
    pagination_state['end_cnt'] = min(pagination_state['total_cnt'], (25 * page))
    pagination_state['page'] = page
    pagination_state['pages'] = int((pagination_state['total_cnt'] / 25) + 1)

    languages = Language.query.order_by(Language.name).all()

    return render_template('search_page.html',
            form=form,
            results=results,
            query_state=query_state,
            pagination_state=pagination_state,
            languages=languages)
