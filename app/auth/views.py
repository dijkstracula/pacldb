from flask import flash, render_template
from . import auth_blueprint

from app import User
from .forms import LoginForm

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # POST
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or user.verify_password(form.password.data):
            flash('Invalid username or password.', 'danger')
            return render_template('auth/login.html', form=form)
        login_user(user, form.remember_me.data)
        return redirect(url_for('main.index'))
    else:
        # GET
        return render_template('auth/login.html', form=form)
