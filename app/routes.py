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

    if form.validate_on_submit():
        return redirect(url_for('main.search_page',
            concept=form.concept.data,
            term=form.term.data,
            gloss=form.gloss.data))

    #XXX: is there a way to auto-populate a form given the request object?
    concept = form.concept.data = request.args.get('concept')
    term = form.term.data = request.args.get('term')
    gloss = form.gloss.data = request.args.get('gloss')

    query = Term.query.join(Concept).join(Language).join(Gloss).order_by(asc(func.lower(Concept.name)))
    if concept:
        query = query.filter(Concept.name.like(concept.strip()))
    if term:
        query = query.filter(Term.text.like(term.strip()))
    if gloss:
        query = query.filter(Gloss.gloss.like(gloss.strip()))

    results = query.paginate(page=page, per_page=25)
    results.total = query.count() #XXX: why do I have to manually set this?

    pagination_state = {}
    pagination_state["next_url"] = url_for('main.search_page',
            page=results.next_num,
            concept=concept,
            term=term,
            gloss=term) \
        if results.has_next else None
    pagination_state["prev_url"] = url_for('main.search_page',
            page=results.prev_num,
            concept=concept,
            term=term,
            gloss=gloss) \
        if results.has_prev else None

    pagination_state['begin_cnt'] = (1 + (25 * (page-1)))
    pagination_state['end_cnt'] = min(results.total, (25 * page))
    pagination_state['page'] = page
    pagination_state['pages'] = int((results.total / 25) + 1)

    return render_template('search_page.html',
            form=form,
            results=results,
            pagination_state=pagination_state)
