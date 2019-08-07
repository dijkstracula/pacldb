from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app.models import Morph, Language

def get_langs():
    return Language.query.order_by(Language.name)

def get_morphs():
    return Morph.query.order_by(Morph.name)

class SearchForm(FlaskForm):
    concept = StringField('concept')
    morph_type = QuerySelectField('morph_type', query_factory=get_morphs, allow_blank=True, get_label="name")
    term = StringField('term')
    gloss = StringField('gloss')
    language = QuerySelectField('language', query_factory=get_langs, allow_blank=True, get_label="name")
    submit = SubmitField('Search')
