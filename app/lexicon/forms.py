from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app.models import Domain, Morph, Language

def get_domains():
    return Domain.query.order_by(Domain.name)

def get_langs():
    return Language.query.order_by(Language.name)

def strip_whitespace(value):
    if value is not None and hasattr(value, 'strip'):
        return value.strip()
    return value

# TODO: is this any different from SearchForm? Should we merge the two?
class LexiconForm(FlaskForm):
    id = StringField('id')
    created_by = StringField("created_by")
    last_edited_by = StringField("last_edited_by")
    last_edited_on = StringField("last_edited_on")
    domain = QuerySelectField('domain', query_factory=get_domains, allow_blank=True, get_label="name", blank_text="-all-")
    concept = StringField('concept', filters=[strip_whitespace])
    morph = StringField('morph', filters=[strip_whitespace])
    orthography = StringField('orthography', filters=[strip_whitespace])
    stem_form = StringField('stem_form', filters=[strip_whitespace])
    ipa = StringField('ipa', filters=[strip_whitespace])
    gloss = StringField('gloss', filters=[strip_whitespace])
    literal_gloss = StringField('literal_gloss', filters=[strip_whitespace])
    language = QuerySelectField('language', query_factory=get_langs, allow_blank=True, get_label="name", blank_text="-all-")

    comment = TextAreaField(u'Comment')
    submit = SubmitField('Search')
