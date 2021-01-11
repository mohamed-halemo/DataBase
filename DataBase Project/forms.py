from flask_wtf import FlaskForm
from flask_wtf import Form

from wtforms import StringField, PasswordField,SubmitField,BooleanField, TextField, TextAreaField, SubmitField

from wtforms.validators import DataRequired, Length, Email,EqualTo
import email_validator
#from wtforms import TextField, TextAreaField, SubmitField

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')


class ContactForm(Form):

    name = TextField("Name")
    email = TextField("Email")
    subject = TextField("Subject")
    message = TextAreaField("Message")
    submit = SubmitField("Send")

