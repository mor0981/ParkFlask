from flask_wtf import FlaskForm
<<<<<<< HEAD
<<<<<<< HEAD
from wtforms import StringField, PasswordField , SubmitField , RadioField,TextAreaField
=======
from wtforms import StringField, PasswordField , SubmitField , RadioField,TextAreaField,TextField
>>>>>>> 028b9f3dfcc70c0de62b07d0f9ec9f38e34470b7
=======
from wtforms import StringField, PasswordField , SubmitField , RadioField,TextAreaField,TextField
>>>>>>> 2c5acab3c06d869bb00b403aeea9782668cdba44
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

class ElementsForm(FlaskForm):
    parkName = StringField("שם הפארק", validators=[DataRequired()])
    parkAddress = StringField("כתובת הפארק", validators=[DataRequired()])
    submit = SubmitField('מחק פארק')

class signupForm(FlaskForm):
    email = StringField("דואר אלקטרוני")
    password= PasswordField("סיסמא")
    username = StringField("שם משתמש")
    submit=SubmitField("הרשם")

class signout2Form(FlaskForm):
    email = StringField("דואר אלקטרוני")
    password= PasswordField("סיסמא")
    username = StringField("שם משתמש")
    submit=SubmitField("ביטול מנוי")

<<<<<<< HEAD
<<<<<<< HEAD
class addComment(FlaskForm):
    submit = SubmitField('הוסף תגובה')
    comment=TextAreaField("רשום תגובה")
=======
=======
>>>>>>> 2c5acab3c06d869bb00b403aeea9782668cdba44
class commentForm(FlaskForm):
    email = StringField("דואר אלקטרוני")
    password= PasswordField("סיסמא")
    submit=SubmitField("שלח")
    submit2=SubmitField("מחק")

    comment=TextAreaField("תגובה")
    date=StringField("תאריך")
    time=StringField("שעה")
    username=StringField("שם משתמש")
    parkname=StringField("שם הפארק")
<<<<<<< HEAD
>>>>>>> 028b9f3dfcc70c0de62b07d0f9ec9f38e34470b7
=======
>>>>>>> 2c5acab3c06d869bb00b403aeea9782668cdba44
