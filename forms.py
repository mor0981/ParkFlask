from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , SubmitField, RadioField
from wtforms.validators import DataRequired , Length , Email

class LoginForm(FlaskForm):
    email = StringField('אימייל',
                        validators=[DataRequired(),Email()])
    password= PasswordField('סיסמא',
                            validators=[DataRequired()])
    submit = SubmitField('התחבר')

class SignOutForm(FlaskForm):
    submit = SubmitField('התנתק')


class NewParkForm(FlaskForm):
    parkName = StringField("שם הפארק", validators=[DataRequired()])

    parkAddress = StringField("כתובת הפארק", validators=[DataRequired()])

    shadow = RadioField("?הצללה",choices=[('yes','כן'),('no','לא')], validators=[DataRequired()])

    submit = SubmitField('צור פארק')


class DeleteParkForm(FlaskForm):
    parkName = StringField("שם הפארק", validators=[DataRequired()])

    parkAddress = StringField("כתובת הפארק", validators=[DataRequired()])

    submit = SubmitField('מחק פארק')
