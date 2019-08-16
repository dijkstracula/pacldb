from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app.models import Concept, Morph, Language

def get_domains():
    return Concept.query.order_by(Concept.domain)

def get_langs():
    return Language.query.order_by(Language.name)

def get_morphs():
    return Morph.query.order_by(Morph.name)

class SearchForm(FlaskForm):
    domain = QuerySelectField('domain', query_factory=get_domains, allow_blank=True, get_label="name")
    concept = StringField('concept')
    morph_type = QuerySelectField('morph_type', query_factory=get_morphs, allow_blank=True, get_label="name")
    orthography = StringField('orthography')
    stem_form = StringField('stem_form')
    ipa = StringField('ipa')
    gloss = StringField('gloss')
    language = QuerySelectField('language', query_factory=get_langs, allow_blank=True, get_label="name")
    submit = SubmitField('Search')
