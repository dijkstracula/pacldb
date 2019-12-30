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

# TODO: is this any different from SearchForm? Should we merge the two?
class LexiconForm(FlaskForm):
    id = StringField('id')
    last_edited_by = StringField("last_edited_by")
    domain = QuerySelectField('domain', query_factory=get_domains, allow_blank=True, get_label="name", blank_text="-all-")
    concept = StringField('concept')
    morph = QuerySelectField('morph', query_factory=get_morphs, allow_blank=True, get_label="name", blank_text="-all-")
    orthography = StringField('orthography')
    stem_form = StringField('stem_form')
    ipa = StringField('ipa')
    gloss = StringField('gloss')
    literal_gloss = StringField('literal_gloss')
    language = QuerySelectField('language', query_factory=get_langs, allow_blank=True, get_label="name", blank_text="-all-")
    submit = SubmitField('Search')