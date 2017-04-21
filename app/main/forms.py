from flask_wtf import FlaskForm

# Import Form elements
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SubmitField

# Import Form validators
from wtforms.validators import DataRequired, Email, EqualTo

class UploadForm(FlaskForm):
    video = FileField('Video', validators=[FileRequired()])

    title = StringField('Title', [DataRequired(message='Please provide a title for the video')])

    description = TextAreaField('Description')

    submit = SubmitField('Submit')