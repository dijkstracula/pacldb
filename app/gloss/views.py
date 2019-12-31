from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import login_required
from flask import json, jsonify

from app import db
from app.models import Gloss

from .forms import GlossForm

from . import gloss_blueprint

def update_gloss(entry):
    entry.gloss = request.json.get('gloss').strip()
    entry.source = request.json.get('source').strip()
    entry.page = int(request.json.get('page'))

    db.session.commit()

    resp = jsonify(success=True)
    return resp

def delete_gloss(entry):
    db.session.delete(entry)
    db.session.commit()

    resp = jsonify(success=True)
    return resp

@gloss_blueprint.route('/', methods=['POST'])
@login_required
def create_gloss():
    if not request.content_type == 'application/json':
        abort(400)
    if not request.json:
        abort(400, "missing JSON body")

    entry = Gloss()
    entry.term_id = request.json.get('term_id').strip()
    entry.gloss = request.json.get('gloss').strip()
    entry.source = request.json.get('source').strip()
    entry.page = int(request.json.get('page'))

    db.session.add(entry)
    db.session.commit()

    resp = jsonify(success=True)
    return resp

@gloss_blueprint.route('/<int:tid>', methods=['PUT', 'DELETE'])
@login_required
def mutate_gloss(tid):
    if not request.content_type == 'application/json':
        abort(400)
    if not request.json:
        abort(400, "missing JSON body")

    query = Gloss.query
    query = query.filter(Gloss.id == tid)

    result = query.first()
    if not result:
        abort(404)

    if request.method == 'PUT':
        return update_gloss(result)
    elif request.method == 'DELETE':
        return delete_gloss(result);
    abort(503) # shouldn't ever get here, but...


