from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import login_required

from app.models import User

from . import admin_blueprint
from app.decorators import admin_required

@admin_blueprint.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def ortho_page():
    users = User.query.all()
    invitations = Invitation.query.all()
    return render_template('admin/admin_page.html', users=users, invitations=invitations)
