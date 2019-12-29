from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask import json, jsonify

from app.models import Domain, Gloss, Language, Morph, Term

from .forms import LexiconForm

from . import lexicon_blueprint

@lexicon_blueprint.route('/show/<tid>', methods=['GET'])
def orthography_page(tid):
    query = Term.query.join(Language).join(Gloss).join(Domain).join(Morph)
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
                       orthography=result.orthography,
                       stem_form = result.stem_form,
                       ipa = result.ipa,
                       literal_gloss = result.literal_gloss,
                       language = result.language)
    return render_template('lexicon/entry_page.html', result=form, glosses=result.glosses)

