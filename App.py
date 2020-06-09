from flask import Flask,render_template,request,flash,session,redirect,url_for
from forms import LoginForm,SignOutForm,NewParkForm,DeleteParkForm,signupForm,signout2Form,addComment,updateComment,facilitiesForm
import pyrebase
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import firestore
app = Flask(__name__)
app.config['SECRET_KEY']='mormormor'
import json 
import os
import tempfile
from werkzeug.utils import secure_filename


print(firebase_admin)
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
firebase_admin.initialize_app(cred)

db = firestore.client()


firebase = pyrebase.initialize_app(config)
auth= firebase.auth()
storage=firebase.storage()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/',methods=['GET', 'POST'])
@app.route('/homePage',methods=['GET', 'POST'])
def homePage():
        if "user" in session:
            if(session["admin"]):
                return redirect(url_for("adminPage"))
            else:
                return redirect(url_for("visitPage"))
        return render_template('homePage.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    print("login")
    form = LoginForm()
    if request.method == 'POST':
    # if form.validate_on_submit():
        print("click")
        try:
            user=auth.sign_in_with_email_and_password(form.email.data,form.password.data)
            uid=auth.get_account_info(user['idToken'])['users'][0]['localId']
            session["uid"]=uid
            doc_ref=db.collection(u"Users").document(uid)
            doc = doc_ref.get()
            if doc.exists:
                admin=doc.to_dict()['admin']
                if(admin):
                    session["admin"]=True
                    session["user"]=form.email.data
                    return redirect(url_for("adminPage"))
                else:
                    session["admin"]=False
                    session["user"]=form.email.data
                    return redirect(url_for("visitPage"))
        except:
            return render_template('index.html',form=form,us="Not Exist")
    else:
        if "user" in session:
            if(session["admin"]):
                return redirect(url_for("adminPage"))
            else:
                return redirect(url_for("visitPage"))
        print("gggggg")
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
    print("logout")
    session.pop("user",None)
    flash("התנתקת בהצלחה")
    return redirect(url_for("homePage"))

@app.route('/register',methods=['GET', 'POST'])
def register():
    form=signupForm()
    if request.method == 'POST':
        email=form.email.data
        password=form.password.data
        name=form.name.data
        last=form.last.data
        user=auth.create_user_with_email_and_password(email,password)
        data={"name":name,"last":last,"email":email,"password":password,"admin":False}
        #db.child("Guest").push(data)
        #data2={"name":"1","other":email,"shadowing":"123"}
        #db.child("Parks").push(data2)
        print(auth.get_account_info(user['idToken'])['users'][0]['localId'])
        info=auth.get_account_info(user['idToken'])['users'][0]['localId']
        db.collection(u'Users').document(info).set(data)
        return redirect(url_for("login"))
    return render_template('basic.html',form=form)

#signup
@app.route('/signup',methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

#unregister
@app.route('/unregister',methods=['GET', 'POST'])
def unregister():
    form=signout2Form()
    if request.method == 'POST':
        print("in if1")
        email=form.email.data
        password=form.password.data
        docs=db.collection(u'Users').stream()
        for doc in docs:
            d=doc.to_dict()
            if email==d['email'] and password==d['password']:
                user_id=doc.id
                docs = db.collection(u'Comments').where(u'userId', u'==', user_id).stream()
                for doc in docs:
                    doc.reference.delete()
                firebase_admin.auth.delete_user(user_id)
                db.collection(u'Users').document(user_id).delete()
                session.pop("user",None)
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
        return render_template('parks.html',data=data,admin=session["admin"])

@app.route('/comments/<p>',methods=['GET', 'POST'])
def comments(p):
    form=addComment()
    docs = db.collection(u'Comments').where(u'name', u'==', p).stream()
    arr=[]
    for doc in docs:
        d=doc.to_dict()
        d["first"]=db.collection(u'Users').document(d["userId"]).get().to_dict()["name"]
        d["last"]=db.collection(u'Users').document(d["userId"]).get().to_dict()["last"]
        d["post_id"]=doc.id
        arr.append(d)
    if request.method == 'POST':
        data={'name':p,'userId':session["uid"],'text':form.comment.data}
        doc=db.collection(u'Comments').document()
        doc.set(data)
        f = request.files['file']
        if f.filename != '':
            filename = secure_filename(f.filename)
            print(filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            storage.child("image/"+doc.id).put("static/uploads/"+filename)
            url=storage.child("image/"+doc.id).get_url(None)
            doc.update({
                'image':url
            })
        return redirect(request.referrer)
    return render_template('comments.html',admin=session["admin"],parkName=p,email=session["user"],comments=arr,form=form,now=session["uid"])

@app.route('/comments/<post_id>/delete',methods=['GET', 'POST'])
def delete_comments(post_id):
    db.collection(u'Comments').document(post_id).delete()
    return redirect(url_for('parks'))

@app.route('/comments/<post_id>/<text>/update',methods=['GET', 'POST'])
def update_comments(post_id,text):
    form=updateComment()
    if form.validate_on_submit():
        data={'text':form.comment.data}
        db.collection(u'Comments').document(post_id).update(data)
        return redirect(url_for('parks'))
    return render_template('updateComment.html',form=form,admin=session["admin"],text=text)


@app.route('/facilities', methods=['GET', 'POST'])
def facilities():
        form = facilitiesForm()
        if form.validate_on_submit():
            docs = db.collection(u'Parks').stream()
            parkData = {
                "name": form.parkNameDB.data,
                "parkFacility": request.form.getlist('facility')
            }
            canAddPark = False
            for doc in docs:
                dici = doc.to_dict()
                try:
                    if parkData['name'] == dici['name']:
                        canAddPark = True

                    if canAddPark:
                        # Deleting and creating a new park witch will be updated with the new facilities
                        db.collection(u'Parks').document(doc.id).delete()
                        db.collection(u'Parks').document().set(parkData)
                        flash("עדכן מתקנים")
                        break

                except Exception as err:
                    pass
            return redirect(url_for('facilities'))
        return render_template('facilities.html', data=data, admin=session["admin"], form=form)

def addData():
    # UP LOADING ALL PARKS TO FIRE-BASE
    for i in data:
        db.collection(u'Parks').document().set({"name": i['Name']})
        # db.collection(u'Parks').document().set({"name": i['Name'], "Other": i['other']})


#finnish
if __name__ == '__main__':
    app.run(debug=True)


