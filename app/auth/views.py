from flask import render_template
from . import auth_blueprint

from .forms import LoginForm

@auth_blueprint.route('/login')
def login():
    form = LoginForm()

    return render_template('auth/login.html', form=form)
