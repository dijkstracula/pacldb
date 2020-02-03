from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required

from app.models import *

from . import admin_blueprint
from app.decorators import admin_required

from .forms import UserEditForm

@admin_blueprint.route('/edit_user', methods=['POST'])
@login_required
@admin_required
def edit_user():
    form = UserEditForm()
    if form.validate_on_submit():
        user = User.query.get(form.id.data)
        if not User:
            abort(404)

        # We don't want to lock our own account out of being an
        # administrator, so bail if we are trying to set our own
        # account to a guest editor one.
        if current_user.id == user.id:
            if form.is_admin.data == "False":
                flash("Can't downgrade our own account to guest", "warning")
                return redirect(url_for('admin.admin_page'))

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.is_admin = form.is_admin.data == "True"
        db.session.commit()
        flash(f"User {user.id} updated.")
    else:
        for field in form.errors:
            errors = ",".join(form.errors[field])
            msg = "Error processing {}: {}".format(field, errors)
            flash(msg, "danger")

    return redirect(url_for('admin.admin_page'))

@admin_blueprint.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_page():
    users = []
    for user in User.query.order_by(User.id).all():
        f = UserEditForm(
            id = user.id,
            first_name = user.first_name,
            last_name = user.last_name,
            email = user.email,
            is_admin = user.is_admin
        )
        users.append(f)
    invitations = Invitation.query.all()
    return render_template('admin/admin_page.html', users=users, invitations=invitations)
