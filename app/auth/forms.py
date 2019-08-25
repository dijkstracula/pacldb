from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class InviteForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Length(1,64), Email()])
    submit = SubmitField('Log in')

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')
