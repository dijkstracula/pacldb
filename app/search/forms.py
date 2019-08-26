from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app.models import Domain, Morph, Language

def get_domains():
    return Domain.query.order_by(Domain.name)

def get_langs():
    return Language.query.order_by(Language.name)

def get_morphs():
    return Morph.query.order_by(Morph.name)

class SearchForm(FlaskForm):
    domain = QuerySelectField('domain', query_factory=get_domains, allow_blank=True, get_label="name", blank_text="-any-")
    concept = StringField('concept')
    morph_type = QuerySelectField('morph_type', query_factory=get_morphs, allow_blank=True, get_label="name", blank_text="-any-")
    orthography = StringField('orthography')
    stem_form = StringField('stem_form')
    ipa = StringField('ipa')
    gloss = StringField('gloss')
    literal_gloss = StringField('literal_gloss')
    language = QuerySelectField('language', query_factory=get_langs, allow_blank=True, get_label="name", blank_text="-any-")
    sort_column = HiddenField('sort_column')
    submit = SubmitField('Search')
