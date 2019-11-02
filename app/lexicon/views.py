from flask import Blueprint, flash, redirect, render_template, request, url_for, abort

from app.models import Domain, Gloss, Language, Morph, Term

from . import lexicon_blueprint

@lexicon_blueprint.route('/show/<tid>', methods=['GET'])
def orthography_page(tid):
    query = Term.query.join(Language).join(Gloss).join(Domain).join(Morph)
    query = query.filter(Term.id == tid)

    result = query.first()
    if not result:
        abort(404)

    return render_template('lexicon/entry_page.html', result=result)

