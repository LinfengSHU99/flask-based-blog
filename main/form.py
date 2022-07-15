from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField


class MarkDownForm(FlaskForm):
    title = StringField('Title of the article', validators=[DataRequired()])
    subtitle = StringField('Subtitle of the article')
    category = StringField('Chose the category', validators=[DataRequired()])
    tag = StringField('Chose the tag', validators=[DataRequired()])
    password = PasswordField('Input the token', validators=[DataRequired()])
    pagedown = PageDownField('Enter your markdown', validators=[DataRequired()])
    submit = SubmitField('Submit')


class NameForm(FlaskForm):
    name = StringField("name?")
    submit = SubmitField('submit')
