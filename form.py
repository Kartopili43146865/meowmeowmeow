from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.fields import SubmitField, TextAreaField, StringField, PasswordField
from wtforms.validators import DataRequired, Length

class addPost(FlaskForm):
    title = TextAreaField("let's friend know what's on your mind...", validators=[DataRequired()])
    img = FileField('')

    button = SubmitField('Post')


class editPost(FlaskForm):
    title = TextAreaField("let's friend know what's on your mind...")
    img = FileField('')
    button = SubmitField('Edit')


class signUp(FlaskForm):
    name = StringField('name...', validators=[DataRequired(),Length(max=8)])
    password = PasswordField('name...', validators=[DataRequired()])
    pfp = FileField('', validators=[DataRequired()])

    button = SubmitField('')

class loginForm(FlaskForm):
    name = StringField('name...', validators=[DataRequired()])
    password = PasswordField('name...', validators=[DataRequired()])

    button = SubmitField('')

class addComment(FlaskForm):
    comment = TextAreaField("write a comment...", validators=[DataRequired()])

    button = SubmitField('Comment')