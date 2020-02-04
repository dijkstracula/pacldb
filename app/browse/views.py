from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask import json, jsonify

from sqlalchemy import asc, distinct, func

from app.models import Domain, Gloss, Language, Morph, Term

from . import browse_blueprint

from .forms import SearchForm

import re

def table_by_name(name):
    """Not my finest work, but I don't know of a way to extract a class
    from a string that won't leave me paranoid about SQL injection, so
    let's do it the silly way."""
    if name == "domain":
        return Domain.name
    if name == "concept":
        return Term.concept
    if name == "morph":
        return Morph.name
    if name == "ortho":
        return Term.orthography
    if name == "stem":
        return Term.stem_form
    if name == "ipa":
        return Term.ipa
    if name == "language":
        return Language.name
    if name == "literal_gloss":
        return Term.literal_gloss
    raise Exception("Unexpected sort column '{}'. Ignoring.".format(name))

@browse_blueprint.route('/', methods=['GET', 'POST'])
def browse_page():
    page = request.args.get('page', 1, type=int)

    form = SearchForm(request.form)

    if form.validate_on_submit():
        params = {}
        for k in request.form:
            v = request.form[k]
            if v and v != '__None' and v != '':
                params[k] = v
        del params['csrf_token']

        return redirect(url_for('browse.browse_page', **params))

    concept = request.args.get('concept')
    orthography = request.args.get('orthography')
    stem_form = request.args.get('stem_form')
    ipa = request.args.get('ipa')
    gloss = request.args.get('gloss')
    literal_gloss = request.args.get('literal_gloss') or ""

    domain_id = request.args.get('domain_id')
    form.domain.data = Domain.query.filter(Domain.id == domain_id).first()

    language_id = request.args.get('language')
    form.language.data = Language.query.filter(Language.id == language_id).first()

    morph_id = request.args.get('morph')
    form.morph.data = Morph.query.filter(Morph.id == morph_id).first()

    sort_column = form.sort_column.data = request.args.get('sort_column')

    query = Term.query.outerjoin(Language).outerjoin(Gloss).outerjoin(Domain).outerjoin(Morph)

    if domain_id:
        query = query.filter(Domain.id == domain_id)
    if concept:
        query = query.filter(Term.concept.op("~*")(f'(^|[^[:alnum:]]){concept.strip()}($|[^[:alnum:]])'))
    if morph_id:
        query = query.filter(Term.morph_id == morph_id);
    if orthography:
        query = query.filter(Term.orthography.ilike(f'%{orthography.strip()}%'))
    if stem_form:
        query = query.filter(Term.stem_form.ilike(f'%{stem_form.strip()}%'))
    if ipa:
        query = query.filter(Term.ipa.op("~*")(f'{ipa.strip()}'))
    if language_id:
        query = query.filter(Term.language_id == language_id);
    if gloss:
        query = query.filter(Gloss.gloss.ilike(f'%{gloss.strip()}%'))
    if literal_gloss:
        query = query.filter(Term.literal_gloss.ilike(f'%{literal_gloss.strip()}%'))

    if sort_column:
        try:
            query = query.order_by(asc(func.lower(table_by_name(sort_column))))
        except Exception as e:
            # garbage sort column? just ignore it.
            flash(str(e), "warning")
            sort_column = None

    #TODO: page=min(page, query.count())?
    results = query.paginate(page, 100, False)
    results.total = query.count() #XXX: why do I have to manually set this?

    pagination_state = {}
    pagination_state["next_url"] = url_for('browse.browse_page',
            page=results.next_num,
            domain_id=domain_id,
            concept=concept,
            orthography=orthography,
            stem_form=stem_form,
            ipa=ipa,
            language_id=language_id,
            gloss=gloss,
            literal_gloss=literal_gloss,
            sort_column=sort_column) \
        if results.has_next else None
    pagination_state["prev_url"] = url_for('browse.browse_page',
            page=results.prev_num,
            domain_id=domain_id,
            concept=concept,
            orthography=orthography,
            stem_form=stem_form,
            ipa=ipa,
            language_id=language_id,
            literal_gloss=literal_gloss,
            gloss=gloss,
            sort_column=sort_column) \
        if results.has_prev else None

    pagination_state['begin_cnt'] = (1 + (100 * (page-1)))
    pagination_state['end_cnt'] = min(results.total, (100 * page))
    pagination_state['page'] = page
    pagination_state['pages'] = int((results.total / 100) + 1)

    if request.content_type == 'application/json':
        blob = {'results': [i.to_json() for i in results.items],
                'page': page}
        return jsonify(blob)

    return render_template('browse_page.html',
            form=form,
            results=results,
            pagination_state=pagination_state)
