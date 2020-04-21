import firebase_admin
import pyrebase
from flask import Flask, render_template, session, redirect, url_for

from forms import LoginForm, SignOutForm, LoginGuestForm

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('C:\\Users\\th_en\\OneDrive\\מסמכים\\GitHub\\ParkFlask\\parkflask-firebase-adminsdk-wplsp-efcf1923d6.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


app = Flask(__name__)
app.config['SECRET_KEY']='mormormor'

config={
  "apiKey": "AIzaSyDab7tKKm11tgRuLsAPejXGGAYJ1d20cnQ",
  "authDomain": "parkflask.firebaseapp.com",
  "databaseURL": "https://parkflask.firebaseio.com",
  "projectId": "parkflask",
  "storageBucket": "parkflask.appspot.com",
  "messagingSenderId": "685599054335",
  "appId": "1:685599054335:web:db2d1d2890588a14772fca",
  "measurementId": "G-H8HGMEE4WB"
}






firebase = pyrebase.initialize_app(config)
auth= firebase.auth()


@app.route('/',methods=['GET', 'POST'])
@app.route('/home',methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            auth.sign_in_with_email_and_password(form.email.data,form.password.data)
            session["user"]=form.email.data
            return redirect(url_for("user"))
        except:
            return render_template('index.html',form=form,us="Not Exist")
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template('index.html',form=form)

@app.route('/user',methods=['GET', 'POST'])
def user():
    form = SignOutForm()
    if form.validate_on_submit():
        return redirect(url_for("logout"))
    return render_template('home.html',form=form)

@app.route('/logout')
def logout():
    session.pop("user",None)
    return redirect(url_for("home"))

@app.route('/register',methods=['GET', 'POST'])
def register():
    return render_template('basic.html')
"""unregister"""
@app.route('/unregister',methods=['GET', 'POST'])
def unregister():
    return render_template('basic3.html')



@app.route('/loginGuest',methods=['GET', 'POST'])
def loginGuest():
    form = LoginGuestForm()
    '''ref_doc=db.collection(u'Guest').documents()
    doc=ref_doc.where(u'name',u'==',form.emailg)'''
    #ref_doc=db.collection(u'Guest').where(u'name',u'==',form.emailg.data ).stream()
    #print(ref_doc)
    if form.validate_on_submit():
        try:
            ref_doc=db.collection(u'Guest').where(u'name',u'==',form.emailg.data ).get()
            if ref_doc != None:
                session["userGuest"]=form.emailg.data
                return redirect(url_for("userGuest"))
        except:
            return render_template('loginGuest.html',form=form,us="Not Exist")
    else:
        if "user" in session:
            return redirect(url_for("userGuest"))
        return render_template('loginGuest.html',form=form)


@app.route('/userGuest',methods=['GET', 'POST'])
def userGuest():
    form = SignOutForm()
    if form.validate_on_submit():
        return redirect(url_for("logoutGuest"))
    return render_template('GuestHome.html',form=form)

@app.route('/logoutGuest')
def logoutGuest():
    session.pop("userGuest",None)
    return redirect(url_for("loginGuest"))

 
    

        

"""finnish"""
if __name__ == '__main__':
    app.run(debug=True)