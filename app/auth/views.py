from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from . import auth_blueprint

from app import User
from .forms import LoginForm

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # POST
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid username or password.', 'danger')
            return render_template('auth/login.html', form=form)
        login_user(user, form.remember_me.data)
        return redirect(url_for('main.home_page'))
    else:
        # GET
        return render_template('auth/login.html', form=form)

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("main.home_page"))
