from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , SubmitField
from wtforms.validators import DataRequired , Length , Email

class LoginForm(FlaskForm):
    email = StringField('אימייל',
                        validators=[DataRequired(),Email()])
    password= PasswordField('סיסמא',
                            validators=[DataRequired()])
    submit = SubmitField('התחבר')



class LoginGuestForm(FlaskForm):
    emailg=StringField('Email',validators=[DataRequired(),Email()])
    passwordg=PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

class SignOutForm(FlaskForm):
    submit = SubmitField('התנתק')