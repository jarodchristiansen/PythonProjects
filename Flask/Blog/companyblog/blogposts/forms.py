from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired

POST_BODY_LABEL = "Write something"


class PostForm(FlaskForm):
    heading = StringField('Title', validators=[DataRequired()])
    meta_title = StringField('Meta title', validators=[DataRequired()])
    meta_desc = StringField('Meta description', validators=[DataRequired()])
    keywords = StringField('Keywords', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    post = TextAreaField(POST_BODY_LABEL)
    submit = SubmitField('Submit')

class BlogPostForm(FlaskForm):
    heading = StringField('Title', validators=[DataRequired()])
    keywords = StringField('Keywords', validators=[DataRequired()])
    post = TextAreaField(POST_BODY_LABEL)
    title = StringField('Title',validators=[DataRequired()])
    text = TextAreaField('Text',validators=[DataRequired()])
    meta_title = StringField('Meta title', validators=[DataRequired()])
    meta_desc = StringField('Meta description', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField("Post")

