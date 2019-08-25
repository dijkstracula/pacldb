from flask import current_app, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from . import auth_blueprint

from app import db, User
from app.email import send_email
from app.models import Invitation
from .forms import InviteForm, LoginForm

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@auth_blueprint.route('/invite', methods=['GET', 'POST'])
@login_required
def invite():
    form = InviteForm()
    if form.validate_on_submit():
        # POST
        invitation = Invitation(email=form.email.data)
        db.session.add(invitation)
        db.session.commit()

        try:
            token = invitation.generate_secure_token()
            resp = send_email(form.email.data, "Pan-DLC invitation", "auth/email/invite", token=token)
        except Exception as e:
            db.session.rollback()
            flash("Couldn't send invitation ({})".format(e))
            return redirect(url_for("main.home_page"))

        if resp.status_code >= 200 and resp.status_code <= 299:
            flash("Email invitation sent.")
        else:
            flash("Couldn't send invitation (status code {})".format(resp.status_code))
            db.session.rollback()
        return redirect(url_for("main.home_page"))
    else:
        # GET
        return render_template('auth/invite.html', form=form)

@auth_blueprint.route('/register/<token>')
def register(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token.encode('utf-8'))
        invitation = Invitation.query.get(int(data.get('confirm')))
        if not invitation:
            raise Exception("Uh oh...")
        db.session.delete(invitation)
        db.session.commit()
    except Exception as e:
        print(e)
        flash("Invalid token.", "danger")
        return redirect(url_for("main.home_page"))

    flash("Thank you for accepting, " + invitation.email)
    return redirect(url_for("main.home_page"))

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
        flash('Welcome back, {}.'.format(user.first_name or user.email))
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
