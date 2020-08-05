import sys

sys.path.append('..')

from models import userDB
from bookie import bcrypt

from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, url, Length, Email, ValidationError, regexp
from wtforms.fields.html5 import EmailField, URLField
from flask import flash


class BookmarkForm(FlaskForm):
    url = URLField('URL:', validators=[DataRequired(), url()])
    description = StringField('Description:')
    tags = StringField("Tags:")


class SignupForm(FlaskForm):
    name = StringField("Username:",
                       validators=[DataRequired(), Length(min=8, message="Username must be above 8 characters")])
    email = EmailField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[Length(min=8, message="Password must have more than 8 chars")])
    confirm_password = PasswordField('Confirm password:')

    def validate_email(form, field):
        user = userDB.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("email aldready exists")

    def validate_confirm_password(form, field):
        if form.password.data != field.data:
            raise ValidationError("The passwords does not match")


class LoginForm(FlaskForm):
    email = EmailField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField('Password:')
    remember_me = BooleanField("Kepp me logged in")

    def validate(form):
        user = userDB.query.filter_by(email=form.email.data).first()
        print(user.password)
        if user and form.password.data == user.password:
            return True
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            return True
        flash("Incorrect password or email", "error")
        return False
