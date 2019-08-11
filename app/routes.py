from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_user import current_user

from sqlalchemy import asc, distinct, func

from app import forms
from app.models import Concept, Gloss, Language, Morph, Term

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

    language_id = request.args.get('language')
    form.language.data = Language.query.filter(Language.id == language_id).first()

    morph_id = request.args.get('morph_type')
    form.morph_type.data = Morph.query.filter(Morph.id == morph_id).first()

    print("NBT: {}".format(form.morph_type.data))

    query = Term.query.join(Concept).join(Language).join(Gloss).join(Morph).order_by(asc(func.lower(Concept.name)))

    if concept:
        query = query.filter(Concept.name.like(concept.strip()))
    if morph_id:
        query = query.filter(Term.morph_id == morph_id);
    if orthography:
        query = query.filter(Term.orthography.like(orthography.strip()))
    if stem_form:
        query = query.filter(Term.stem_form.like(stem_form.strip()))
    if ipa:
        query = query.filter(Term.ipa.like(ipa.strip()))
    if language_id:
        query = query.filter(Term.language_id == language_id);
    if gloss:
        query = query.filter(Gloss.gloss.like(gloss.strip()))

    results = query.paginate(page=page, per_page=25)
    results.total = query.count() #XXX: why do I have to manually set this?

    pagination_state = {}
    pagination_state["next_url"] = url_for('main.search_page',
            page=results.next_num,
            concept=concept,
            orthography=orthography,
            stem_form=stem_form,
            ipa=ipa,
            language=language,
            gloss=gloss) \
        if results.has_next else None
    pagination_state["prev_url"] = url_for('main.search_page',
            page=results.prev_num,
            concept=concept,
            orthography=orthography,
            stem_form=stem_form,
            ipa=ipa,
            language=language,
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
