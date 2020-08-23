from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    heading = StringField('Title', validators=[DataRequired()])
    meta_title = StringField('Meta title', validators=[DataRequired()])
    meta_desc = StringField('Meta description', validators=[DataRequired()])
    keywords = StringField('Keywords', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    post = TextAreaField('Write something')
    submit = SubmitField('Submit')

class BlogPostForm(FlaskForm):
    heading = StringField('Title', validators=[DataRequired()])
    keywords = StringField('Keywords', validators=[DataRequired()])
    post = TextAreaField('Write something')
    post = TextAreaField('Write something')
    title = StringField('Title',validators=[DataRequired()])
    text = TextAreaField('Text',validators=[DataRequired()])
    meta_title = StringField('Meta title', validators=[DataRequired()])
    meta_desc = StringField('Meta description', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField("Post")

