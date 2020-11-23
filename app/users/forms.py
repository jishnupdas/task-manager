from flask   import current_app
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField
from app.models  import User
from flask_wtf   import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    '''Creating user registration forms'''

    username = StringField('Username',   validators=[DataRequired(), Length(min=2)])
    email    = StringField('Email',      validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    phone    = IntegerField('Phone',     validators=[DataRequired()])
    address  = StringField('Address',    validators=[DataRequired()])
    address2 = StringField('latlong/googlemaps link')
    submit   = SubmitField('Register')
    

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email    = StringField('Email',      validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit   = SubmitField('Login')
