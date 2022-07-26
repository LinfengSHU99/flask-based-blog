from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField


class MarkDownForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle')
    category = StringField('Category', validators=[DataRequired()])
    tag = StringField('Tag (split by comma)', )
    # password = PasswordField('Token', validators=[DataRequired()])
    pagedown = PageDownField('Enter your markdown', validators=[DataRequired()])
    submit = SubmitField('Submit')


class TestFrom(FlaskForm):
    title = StringField('pw', validators=[DataRequired()])
    submit = SubmitField('submit')
