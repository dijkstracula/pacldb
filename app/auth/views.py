from flask import current_app, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from . import auth_blueprint

from app import db, User
from app.email import send_email
from app.models import Invitation
from .forms import InviteForm, LoginForm, RegistrationForm

from sqlalchemy.exc import IntegrityError
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def create_invite(form):
    invitation = Invitation(
            email=form.email.data,
            should_be_admin=bool(form.should_be_admin.data))

    existing_user = User.query.filter(User.email == invitation.email).first()
    if existing_user:
        raise Exception("A user with this email address is already registered.")

    # We need the user id to generate the token, so we have to commit
    # opportunistically here.
    db.session.add(invitation)
    db.session.commit()

    try:
        token = invitation.generate_secure_token()
        resp = send_email(
                form.email.data,
                "Invitation to edit the Pan-Dene Comparative Lexicon",
                "auth/email/invite",
                token=token)

        if not (resp.status_code >= 200 and resp.status_code <= 299):
            raise Exception("Got {} from Sendgrid".format(resp.status_code))
    except Exception as e:
        db.session.delete(invitation)
        db.session.commit()
        raise e

@auth_blueprint.route('/invite', methods=['GET', 'POST'])
@login_required
def invite():
    form = InviteForm()
    if form.validate_on_submit():
        # POST
        try:
            create_invite(form)
        except IntegrityError:
            flash("An invitation to this email address has already been extended.", "danger")
            return redirect(url_for("auth.invite"))
        except Exception as e:
            flash("Couldn't send invitation ({}).".format(e), "danger")
            return redirect(url_for("auth.invite"))

        flash("Invitation to {} sent.".format(form.email.data))
        return render_template('auth/invite.html', form=form)
    else:
        # GET
        return render_template('auth/invite.html', form=form)

@auth_blueprint.route('/register/<token>', methods=["GET", "POST"])
def register(token):
    # Get the invitation token.
    try:
        s = Serializer(current_app.config['SECRET_KEY'])
        data = s.loads(token.encode('utf-8'))
        invitation = Invitation.query.get(int(data.get('confirm')))
        if not invitation:
            raise Exception("Unknown token.")
    except Exception as e:
        flash("Error validating token: {}".format(e), "danger")
        return redirect(url_for("main.home_page"))

    form = RegistrationForm()
    if form.validate_on_submit():
        # POST
        try:
            user = User(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=form.password.data,
                    is_admin=invitation.should_be_admin)
            db.session.add(user)
            db.session.delete(invitation)
            db.session.commit()
        except Exception as e:
            flash("Couldn't create user: {}.".format(e), "danger")
            return render_template('auth/register.html',
                    form=form,
                    should_be_admin=invitation.should_be_admin)
        flash("New user created!")
        return redirect(url_for("main.home_page"))
    else:
        # GET
        form.email.data = invitation.email
        return render_template('auth/register.html',
                form=form,
                should_be_admin=invitation.should_be_admin)


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
