from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , SubmitField , RadioField,TextAreaField
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

class signupForm(FlaskForm):
    email = StringField("דואר אלקטרוני")
    password= PasswordField("סיסמא")
    name = StringField("שם פרטי")
    last = StringField("שם משפחה")
    Admin = RadioField("?אדמין",choices=[('true','כן'),('false','לא')], validators=[DataRequired()])
    submit=SubmitField("הרשם")

class signout2Form(FlaskForm):
    email = StringField("דואר אלקטרוני")
    password= PasswordField("סיסמא")
    username = StringField("שם משתמש")
    submit=SubmitField("ביטול מנוי")

class addComment(FlaskForm):
    submit = SubmitField('הוסף תגובה')
    comment=TextAreaField("רשום תגובה")

class updateComment(FlaskForm):
    submit = SubmitField('הוסף תגובה')
    comment=TextAreaField("עדכן תגובה")

class facilitiesForm(FlaskForm):
    parkName = StringField("שם הפארק")
    parkNameDB = StringField("שם הפארק")
    facilities = StringField("מתקנים")
    submit = SubmitField('אישור')

class PostForm(FlaskForm):
    email = StringField('איימל', validators=[DataRequired()])
    name = StringField('שם משתמש', validators=[DataRequired()])
    last = StringField('שם משפחה', validators=[DataRequired()])
    password= PasswordField("סיסמא")
    submit = SubmitField('עדכן')