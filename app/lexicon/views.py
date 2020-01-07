from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import login_required
from flask import json, jsonify

from app import db
from app.models import Domain, Gloss, Language, Morph, Term

from .forms import LexiconForm

from . import lexicon_blueprint

def update_ortho(entry, form):
    entry.domain = form.domain.data
    entry.concept = form.concept.data
    entry.morph = form.morph.data
    entry.orthography = form.orthography.data
    entry.stem_form = form.stem_form.data
    entry.ipa = form.ipa.data
    entry.literal_gloss = form.literal_gloss.data
    entry.language = form.language.data

    db.session.commit()
    flash(f"Orthography {entry.id} updated.")

def insert_ortho(form):
    entry = Term()
    entry.domain = form.domain.data
    entry.concept = form.concept.data
    entry.morph = form.morph.data
    entry.orthography = form.orthography.data
    entry.stem_form = form.stem_form.data
    entry.ipa = form.ipa.data
    entry.literal_gloss = form.literal_gloss.data
    entry.language = form.language.data

    db.session.add(entry)
    db.session.commit()
    flash(f"Orthography {entry.id} created!")

@lexicon_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def create_page():
    form = LexiconForm(request.form)
    if form.validate_on_submit():
        insert_ortho(form)

    return render_template('lexicon/entry_page.html', result=form)

@lexicon_blueprint.route('/<tid>', methods=['GET', 'POST'])
@login_required
def orthography_page(tid):
    query = Term.query.join(Language).outerjoin(Gloss).join(Domain).join(Morph)
    query = query.filter(Term.id == tid)
    result = query.first()
    if not result:
        abort(404)

    if request.content_type == 'application/json':
        blob = result.to_json()
        return jsonify(blob)

    form = LexiconForm(id = result.id,
                       last_edited_by = "TODO",
                       domain = result.domain,
                       concept = result.concept,
                       morph = result.morph,
                       morph_id = result.morph,
                       orthography=result.orthography,
                       stem_form = result.stem_form,
                       ipa = result.ipa,
                       literal_gloss = result.literal_gloss,
                       language = result.language)

    if form.validate_on_submit():
        update_ortho(result, form)

    return render_template('lexicon/entry_page.html', result=form, glosses=result.glosses)

