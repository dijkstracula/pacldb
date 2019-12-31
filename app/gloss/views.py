from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import login_required
from flask import json, jsonify

from app import db
from app.models import Gloss

from .forms import GlossForm

from . import gloss_blueprint

def err_response(msg, status=400):
    response = jsonify({
        'status': status,
        'message': msg
    })
    response.status_code = status
    return response

def update_gloss(entry):
    try:
        entry.gloss = request.json.get('gloss').strip()
    except Exception:
        return err_response("Missing or invalid gloss")

    try:
        entry.source = request.json.get('source').strip()
    except Exception:
        return err_response("Missing or invalid citation source")

    try:
        entry.page = int(request.json.get('page'))
    except Exception:
        return err_response("Missing or invalid citation page")

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
        return err_response("Missing JSON body")

    entry = Gloss()

    try:
        entry.term_id = request.json.get('term_id').strip()
    except Exception:
        return err_response("Missing or invalid term ID")

    try:
        entry.gloss = request.json.get('gloss').strip()
    except Exception:
        return err_response("Missing or invalid gloss")

    try:
        entry.source = request.json.get('source').strip()
    except Exception:
        return err_response("Missing or invalid citation source")

    try:
        entry.page = int(request.json.get('page'))
    except Exception:
        return err_response("Missing or invalid citation page")

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
        return err_response("Missing JSON body")

    query = Gloss.query
    query = query.filter(Gloss.id == tid)

    result = query.first()
    if not result:
        return err_response("Gloss not found!", 404)

    if request.method == 'PUT':
        return update_gloss(result)
    elif request.method == 'DELETE':
        return delete_gloss(result);
    abort(503) # shouldn't ever get here, but...


