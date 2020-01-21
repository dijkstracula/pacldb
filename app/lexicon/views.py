from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required
from flask import json, jsonify

from app import db
from app.models import Domain, Gloss, Language, Morph, Term, User

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
    entry.last_edited_by = current_user
    entry.comment = form.comment.data

    db.session.commit()
    flash(f"Orthography {entry.id} updated.")
    return entry

def insert_ortho(form):
    if not form.domain.data:
        raise Exception("Missing domain")
    if not form.language.data:
        raise Exception("Missing language")
    if not form.morph.data:
        raise Exception("Missing morphology")

    entry = Term()
    entry.domain = form.domain.data
    entry.concept = form.concept.data
    entry.morph = form.morph.data
    entry.orthography = form.orthography.data
    entry.stem_form = form.stem_form.data
    entry.ipa = form.ipa.data
    entry.literal_gloss = form.literal_gloss.data
    entry.language = form.language.data
    entry.last_edited_by = current_user
    entry.comment = form.comment.data

    db.session.add(entry)
    db.session.commit()
    flash(f"Orthography {entry.id} created!")
    return entry

def delete_ortho(entry):
    db.session.delete(entry)
    db.session.commit()

    return jsonify({
        'message': "OK"
    })

@lexicon_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def create_page():
    form = LexiconForm(request.form)
    if form.validate_on_submit():
        try:
            entry = insert_ortho(form)
        except Exception as e:
            flash(str(e), "danger")
            return render_template('lexicon/entry_page.html', result=form)
        return redirect(url_for('lexicon.orthography_page', tid=entry.id))

    return render_template('lexicon/entry_page.html', result=form)

@lexicon_blueprint.route('/<tid>', methods=['GET', 'POST', 'DELETE'])
@login_required
def orthography_page(tid):
    query = Term.query.outerjoin(Language).outerjoin(Gloss).outerjoin(Domain).outerjoin(Morph)
    query = query.filter(Term.id == tid)
    result = query.first()
    if not result:
        abort(404)
    if request.method == 'DELETE':
        return delete_ortho(result)

    if not result.created_by:
        created_by = "unknown"
    else:
        created_by = result.created_by.formatted()

    if not result.last_edited_by:
        edited_by = "unknown"
    else:
        edited_by = result.last_edited_by.formatted()

    form = LexiconForm(id = result.id,
                       created_by = created_by,
                       last_edited_by = edited_by,
                       last_edited_on = result.last_edited_on or "unknown",
                       domain = result.domain,
                       concept = result.concept,
                       morph = result.morph,
                       morph_id = result.morph,
                       orthography=result.orthography,
                       stem_form = result.stem_form,
                       ipa = result.ipa,
                       literal_gloss = result.literal_gloss,
                       language = result.language,
                       comment = result.comment)

    if form.validate_on_submit():
        update_ortho(result, form)

    if request.content_type == 'application/json':
        blob = result.to_json()
        return jsonify(blob)

    return render_template('lexicon/entry_page.html', result=form, glosses=result.glosses)

