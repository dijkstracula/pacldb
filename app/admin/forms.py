from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Email

class UserEditForm(FlaskForm):
    id = IntegerField('id', validators = [DataRequired()], render_kw={'readonly':'readonly'},)
    first_name = StringField('First Name')
    last_name = StringField('Last name')
    email = StringField('Email', validators = [DataRequired(), Length(1,64), Email()])
    is_admin = SelectField('Type', choices=[("True", 'Administrator'), ("False", 'Guest Editor')])
    submit = SubmitField('Save')
