from flask import Flask,render_template,request,flash,session,redirect,url_for
from forms import LoginForm,SignOutForm
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)
app.config['SECRET_KEY']='mormormor'


cred = credentials.Certificate('C:\\Users\\mor09\\Desktop\\scholl\\Parck\\parkflask-firebase-adminsdk-wplsp-87a9bb6106.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

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
            user=auth.sign_in_with_email_and_password(form.email.data,form.password.data)
            print(auth.get_account_info(user['idToken'])['users'][0]['localId'])
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
    if "user" in session:
        form = SignOutForm()
        if form.validate_on_submit():
            return redirect(url_for("logout"))
        return render_template('home.html',form=form)
    else:
        return redirect(url_for("home"))

@app.route('/logout')
def logout():
    session.pop("user",None)
    return redirect(url_for("home"))

@app.route('/register',methods=['GET', 'POST'])
def register():
    return render_template('basic.html')

#signup
@app.route('/signup',methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

#unregister
@app.route('/unregister',methods=['GET', 'POST'])
def unregister():
    return render_template('basic3.html')

#finnish
if __name__ == '__main__':
    app.run(debug=True)
