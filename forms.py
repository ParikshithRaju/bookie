from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import DataRequired, url


class BookmarkForm(FlaskForm):
    url = StringField('URL:', validators=[DataRequired(), url()])
    description = StringField('Description:')