from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SearchForm(FlaskForm):
    concept = StringField('Concept')
    term = StringField('Term')
    gloss = StringField('Gloss')
    submit = SubmitField('Search')
