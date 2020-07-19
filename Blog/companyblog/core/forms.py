from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired



class TextGenForm(FlaskForm):
    seed_text = StringField('Seed', validators=[DataRequired()])
    submit = SubmitField('Submit')
class PostForm(FlaskForm):
    heading = StringField('Title', validators=[DataRequired()])
    post = TextAreaField('Write something')
    tags = StringField('Tags')
    submit = SubmitField('Submit')