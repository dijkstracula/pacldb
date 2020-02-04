from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Email

class InviteForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Length(1,64), Email()])
    should_be_admin = BooleanField('Invite user as administrator')
    submit = SubmitField('Invite')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Length(1,64), Email()])
    first_name = StringField("First name")
    last_name = StringField("Last name")
    password = PasswordField('Password', validators=[
            DataRequired(), EqualTo('password2', message='Passwords must match.')
    ])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')
