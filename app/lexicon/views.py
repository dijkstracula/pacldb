from flask import Blueprint, flash, redirect, render_template, request, url_for, abort

from app.models import Concept, Domain, Gloss, Language, Morph, Term

from . import lexicon_blueprint

@lexicon_blueprint.route('/<ortho>', methods=['GET', 'POST'])
def ortho_page(ortho):
    query = Term.query.join(Concept).join(Language).join(Gloss).join(Domain).join(Morph)
    query = query.filter(Term.orthography == ortho)

    result = query.first()
    if not result:
        abort(404)

    return render_template('lexicon/entry_page.html', result=result)