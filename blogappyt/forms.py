from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField,FileAllowed
from .models import User,Post
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('UserName',validators = [DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators = [DataRequired(),Email()])
    password = PasswordField('Password', validators= [DataRequired(),Length(min=8)])
    confirmpassword = PasswordField('Confirm Password', validators= [DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username Taken Please Try Different Username')

    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email Already Registered Please Try Another Email')

class LoginForm(FlaskForm):
    email = StringField('Email',validators = [DataRequired(),Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    rememberme = BooleanField('Remember Me')
    submit = SubmitField('Log in')

class UpdateProfileForm(FlaskForm):
    username = StringField('UserName',validators = [DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators = [DataRequired(),Email()])
    profilepic = FileField('Update Profile Picture',validators = [FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')
    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Username Taken Please Try Different Username')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Email Already Registered Please Try Another Email')


class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email',validators = [DataRequired(),Email()])
    submit = SubmitField('Verify')

    def verify_email(self,email):
        user = User.query.filter_by(email=email.data).first()

        if user is None:
            raise ValidationError('There is no account with this email, Please create an account')


class ResetpasswordForm(FlaskForm):
    password = PasswordField('New Password', validators = [DataRequired()])
    confirmpassword = PasswordField('Confirm Password', validators= [DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset')