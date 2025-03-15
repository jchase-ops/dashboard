from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField, SubmitField, IntegerField

__all__ = ['LoginForm', 'AddUserForm', 'AddPostForm', 'EditPostForm', 'DeletePostForm']


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email_address = StringField('Email')
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = StringField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditPostForm(FlaskForm):
    post_id = IntegerField('Post ID', validators=[DataRequired()])
    title = StringField('Title')
    body = StringField('Body')
    submit = SubmitField('Submit')


class DeletePostForm(FlaskForm):
    post_id = IntegerField('Post ID', validators=[DataRequired()])
    title = StringField('Title')
    body = StringField('Body')
    submit = SubmitField('Submit')