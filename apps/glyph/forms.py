from flask.ext.wtf import Form
from wtforms import (
    TextAreaField,
    StringField,
    validators
)



class SearchForm(Form):
    search = StringField('Search', validators=[validators.DataRequired()])
