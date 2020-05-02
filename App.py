from flask import Flask,render_template,request,flash,session,redirect,url_for
from forms import LoginForm,SignOutForm,NewParkForm,DeleteParkForm,signupForm,signout2Form
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
app = Flask(__name__)
app.config['SECRET_KEY']='mormormor'
import json 


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

with open('playgrounds.json', 'r',encoding="utf8") as myfile:
    data=json.loads(myfile.read())

cred = credentials.Certificate('parkflask-firebase-adminsdk-wplsp-87a9bb6106.json')
print(cred)
firebase_admin.initialize_app(cred)

db = firestore.client()

firebase = pyrebase.initialize_app(config)
auth= firebase.auth(



@app.route('/',methods=['GET', 'POST'])
@app.route('/homePage',methods=['GET', 'POST'])
def homePage():
        return render_template('homePage.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user=auth.sign_in_with_email_and_password(form.email.data,form.password.data)
            uid=auth.get_account_info(user['idToken'])['users'][0]['localId']
            doc_ref=db.collection(u"Users").document(uid)
            doc = doc_ref.get()
            if doc.exists:
                admin=doc.to_dict()['admin']
                if(admin):
                    session["admin"]=True
                    return redirect(url_for("adminPage"))
                else:
                    session["user"]=form.email.data
                    return redirect(url_for("visitPage"))
            else:
                print(u'No such document!')
            # session["user"]=form.email.data
            # return redirect(url_for("user"))
        except:
            return render_template('index.html',form=form,us="Not Exist")
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template('index.html',form=form)



@app.route('/adminPage',methods=['GET', 'POST'])
def adminPage():
        return render_template('adminPage.html')

@app.route('/visitPage',methods=['GET', 'POST'])
def visitPage():
        return render_template('visitPage.html')



@app.route('/user',methods=['GET', 'POST'])
def user():
    if "user" in session:
        form = SignOutForm()
        if form.validate_on_submit():
            return redirect(url_for("logout"))
        return render_template('login.html',form=form)
    else:
        return redirect(url_for("login"))

@app.route('/logout')
def logout():
    session.pop("user",None)
    return redirect(url_for("homePage"))

@app.route('/register',methods=['GET', 'POST'])
def register():
    form=signupForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        username=form.username.data
        user=auth.create_user_with_email_and_password(email,password)
        data={"username":username,"email":email,"password":password,"admin":False}
        #db.child("Guest").push(data)
        #data2={"name":"1","other":email,"shadowing":"123"}
        #db.child("Parks").push(data2)
        print(auth.get_account_info(user['idToken'])['users'][0]['localId'])
        info=auth.get_account_info(user['idToken'])['users'][0]['localId']
        db.collection(u'Users').document(info).set(data)

        return redirect(url_for("visitPage"))
    return render_template('basic.html',form=form)

#signup
@app.route('/signup',methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

#unregister
@app.route('/unregister',methods=['GET', 'POST'])
def unregister():
    form=signout2Form()
    if form.validate_on_submit():
        print("in if1")
        email=form.email.data
        print(email)
        password=form.password.data
        username=form.username.data
        docs=db.collection(u'Users').stream()
        for doc in docs:
            d=doc.to_dict()
            print(d)
            if email==d['email'] and password==d['password']:
                print("if2")
                db.collection(u'Users').document(doc.id).delete()
                return redirect(url_for("homePage"))
        #user=auth.create_user_with_email_and_password(email,password)
        #data={"username":username,"email":email,"password":password}
        #db.child("Guest").push(data)
        #data2={"name":"1","other":email,"shadowing":"123"}
        #db.child("Parks").push(data2)
        #print(auth.get_account_info(user['idToken'])['users'][0]['localId'])
        #info=auth.get_account_info(user['idToken'])['users'][0]['localId']
        #db.collection(u'Guest').document(info).set(data)

    print("hello")
    return render_template('basic3.html',form=form)

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

@app.route('/parks',methods=['GET', 'POST'])
def parks():
        return render_template('parks.html',data=data)

#finnish
if __name__ == '__main__':
    app.run(debug=True)


