from flask import Flask,render_template,request,flash,session,redirect,url_for
from forms import LoginForm,SignOutForm, NewParkForm, DeleteParkForm
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)
app.config['SECRET_KEY']='mormormor'
# Use a service account

# default_app = firebase_admin.initialize_app()

cred = credentials.Certificate('C:\\Users\\Moran Lavi\\Documents\\GitHub\\ParkFlask\\parkflask-firebase-adminsdk-wplsp-78f1875805.json')
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
auth = firebase.auth()

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
    return redirect(url_for("home")

@app.route('/newpark', methods =['GET','POST'])
def newpark():

    form = NewParkForm()
    if form.validate_on_submit():

        data = {
        "name": form.parkName.data,
        "other": form.parkAddress.data,
        "shadowing": form.shadow.data
        }
        docs = db.collection(u'Parks').stream()
        canMakePark = True
        for doc in docs:
            dici = doc.to_dict()
            if data["name"] == dici['name'] and data["other"] == dici['other']:
                canMakePark = False

        if canMakePark:
            db.collection(u'Parks').document().set(data)
            flash(" יצרת פארק חדש ")
        else:
            flash("לא ניתן ליצור פארק")


        return redirect(url_for('newpark'))
    return render_template('createNewPark.html', form=form)


@app.route('/deletepark', methods =['GET','POST'])
def deletepark():

    form = DeleteParkForm()
    if form.validate_on_submit():

        req = request.form
        parkName = req["parkName"]
        parkAddress = req["parkAddress"]

        docs = db.collection(u'Parks').stream()
        for doc in docs:
            dici = doc.to_dict()
            if parkName == dici['name'] and parkAddress == dici['other']:
                print (f"park {dici['name']} in {dici['other']} has beem deleted")
                db.collection(u'Parks').document(doc.id).delete()
                flash("מחקת פארק")


        return redirect(url_for('deletepark'))
    return render_template('deletePark.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
