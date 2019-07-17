from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SearchForm(FlaskForm):
    concept = StringField('Concept')
    term = StringField('Term')
    submit = SubmitField('Search')
