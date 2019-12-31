from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app.models import Gloss

class GlossForm(FlaskForm):
    id = StringField('id')
    gloss = StringField('gloss')
    source = StringField('source')
    page = StringField('page')
