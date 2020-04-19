from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , SubmitField
from wtforms.validators import DataRequired , Length , Email

class LoginForm(FlaskForm):
    email = StringField('אימייל',
                        validators=[DataRequired(),Email()])
    password= PasswordField('סיסמא',
                            validators=[DataRequired()])
    submit = SubmitField('התחבר')

class SignOutForm(FlaskForm):
    submit = SubmitField('התנתק')

class registerForm(FlaskForm):
    Email=StringField("דואר אלקטרוני", validators=[DataRequired(),Email()])
    password= PasswordField('סיסמא',validators=[DataRequired()])
    username=StringField('שם משתמש',validators=[DataRequired()])


class testForm(FlaskForm):
    email=StringField()
    password=StringField()
    submit=SubmitField("button")
