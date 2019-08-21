from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_user import current_user

from sqlalchemy import asc, distinct, func

from app import forms
from app.models import Concept, Domain, Gloss, Language, Morph, Term

import re

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
            domain_id=form.domain.data,
            concept=form.concept.data,
            morph_type=form.morph_type.data,
            orthography=form.orthography.data,
            stem_form=form.stem_form.data,
            ipa=form.ipa.data,
            language=form.language.data,
            gloss=form.gloss.data))

    #XXX: is there a way to auto-populate a form given the request object?
    concept = form.concept.data = request.args.get('concept')
    orthography = form.orthography.data = request.args.get('orthography')
    stem_form = form.stem_form.data = request.args.get('stem_form')
    ipa = form.ipa.data = request.args.get('ipa')
    gloss = form.gloss.data = request.args.get('gloss')

    domain_id = request.args.get('domain_id')
    form.domain.data = Domain.query.filter(Domain.id == domain_id).first()

    language_id = request.args.get('language')
    form.language.data = Language.query.filter(Language.id == language_id).first()

    morph_id = request.args.get('morph_type')
    form.morph_type.data = Morph.query.filter(Morph.id == morph_id).first()

    #query = Term.query.join(Concept).join(Language).join(Gloss).join(Domain).join(Morph).order_by(asc(func.lower(Concept.name)))
    query = Term.query.join(Concept).join(Language).join(Gloss).join(Domain).join(Morph)

    if domain_id:
        query = query.filter(Domain.id == domain_id)
    if concept:
        query = query.filter(Concept.name.op("~*")(f'(^|[^[:alnum:]]){concept.strip()}($|[^[:alnum:]])'))
    if morph_id:
        query = query.filter(Term.morph_id == morph_id);
    if orthography:
        query = query.filter(Term.orthography.ilike(f'{orthography.strip()}'))
    if stem_form:
        query = query.filter(Term.stem_form.ilike(f'%{stem_form.strip()}%'))
    if ipa:
        query = query.filter(Term.ipa.op("~*")(f'{ipa.strip()}'))
    if language_id:
        query = query.filter(Term.language_id == language_id);
    if gloss:
        query = query.filter(Gloss.gloss.ilike(f'{gloss.strip()}'))

    results = query.paginate(page=page, per_page=100)
    results.total = query.count() #XXX: why do I have to manually set this?

    pagination_state = {}
    pagination_state["next_url"] = url_for('main.search_page',
            page=results.next_num,
            domain_id=domain_id,
            concept=concept,
            orthography=orthography,
            stem_form=stem_form,
            ipa=ipa,
            language_id=language_id,
            gloss=gloss) \
        if results.has_next else None
    pagination_state["prev_url"] = url_for('main.search_page',
            page=results.prev_num,
            domain_id=domain_id,
            concept=concept,
            orthography=orthography,
            stem_form=stem_form,
            ipa=ipa,
            language_id=language_id,
            gloss=gloss) \
        if results.has_prev else None

    pagination_state['begin_cnt'] = (1 + (100 * (page-1)))
    pagination_state['end_cnt'] = min(results.total, (100 * page))
    pagination_state['page'] = page
    pagination_state['pages'] = int((results.total / 100) + 1)

    return render_template('search_page.html',
            form=form,
            results=results,
            pagination_state=pagination_state)
