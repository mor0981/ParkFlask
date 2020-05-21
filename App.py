from flask import Flask,render_template,request,flash,session,redirect,url_for
<<<<<<< Updated upstream
<<<<<<< HEAD
from forms import LoginForm,SignOutForm,NewParkForm,DeleteParkForm,signupForm,signout2Form,addComment,updateComment,facilitiesForm
=======

=======

>>>>>
<<<<<<< Updated upstream
=======
>>>>>>> ab1471228fe146bf16f41e5a8183d11a56f0e97a
>>>>>>> Stashed changes
=======
from forms import LoginForm,SignOutForm,NewParkForm,DeleteParkForm,signupForm,signout2Form,addComment,updateComment,facilitiesForm
>>>>>>> Stashed changes
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
auth= firebase.auth()


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
    form = LoginForm()
    if form.validate_on_submit():
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
    if form.validate_on_submit():
        data={'name':p,'userId':session["uid"],'text':form.comment.data}
        db.collection(u'Comments').document().set(data)
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


<<<<<<< Updated upstream
<<<<<<< HEAD
=======


x=0
def idcount():
    global x
    x += 1
    return x

@app.route("/comment/new", methods=['GET', 'POST'])
def new_comment_Guset():
    form=PostForm()
    data = {
    "post_id":idcount(),
    "title":form.title.data,
    "content": form.content.data,
    "author": session["user"]
    }
    #db.collection(u'Comments').document().set(data)
    #docs = db.collection(u'Comments').stream()
    if form.validate_on_submit():
        db.collection(u'testComments').document().set(data)
        #newPostRef=db.collection(u'testComments').
        #post_id = newPostRef.key
        flash(" תגובה נשלחה  ")
        return redirect(url_for('new_comment_Guset'))
    return render_template('CreateParkComment.html', title='New comment',
                           form=form, legend='New Comment')




@app.route("/comment/<int:post_id>")
def Comment_guest(post_id):
    #post=db.collection(u'testComments').query.get_or_404(post_id)
    post=db.collection(u'testComments').where(u'post_id',u'==',post_id).stream()

   # rpost=post.to_dict()['title']
    docs = db.collection(u'testComments').stream()
    canMakePark = True
    print(post_id)

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
    if form.validate_on_submit():
        data={'name':p,'userId':session["uid"],'text':form.comment.data}
        db.collection(u'Comments').document().set(data)
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


@app.route("/comment/<int:post_id>/update", methods=['GET', 'POST'])
def update_comment_guest(post_id):
    #post=db.collection(u'testComments').query.get_or_404(post_id)
    docs = db.collection(u'testComments').stream()
    canMakePark = True
    for doc in docs:
        dici = doc.to_dict()
        if  dici['post_id']==post_id :
            canMakePark = False
            rpost=dici['title']
            idpost=dici['post_id']
            print(idpost)
            wanted=dici
    if canMakePark:
        abort(403)
           
    else:
        rrpost=rpost
    ref_comment=db.collection(u'testComments')
    ref_my=ref_comment.where(u'post_id',u'==',post_id).stream()
    for r in ref_my:
        rr=r.to_dict()['post_id']
        print(rr)
    #if post.author != session['user']:
     #   abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post_title = form.title.data
        post_content = form.content.data
        ref_comment=db.collection(u'testComments')
        ref_my=ref_comment.where(u'post_id',u'==',post_id).get()
        field_updates={"title":form.title.data,"content":form.content.data}
        for r in ref_my:
            rr=ref_comment.document(r.id)
            rr.update(field_updates)
        
        flash('Your comment has been updated!', 'success')
        return redirect(url_for('parkHome', post_id=idpost))
    elif request.method == 'GET':
        docs
        form.title.data = wanted['title']
        form.content.data = wanted['content']
    return render_template('CreateParkComment.html', title='Update Comment',
                           form=form, legend='Update Comment')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_comment_guest(post_id):
    ref_comment=db.collection(u'testComments')
    ref_my=ref_comment.where(u'post_id',u'==',post_id).get()
    for r in ref_my:
        rr=ref_comment.document(r.id)
        rr.delete()
    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('parkHome'))




@app.route("/")
@app.route("/parkHome",methods=['GET','POST'])
def parkHome():
    posts = db.collection(u'testComments').stream()
    return render_template('parkHome.html', posts=posts)
>>>>>>> ab1471228fe146bf16f41e5a8183d11a56f0e97a
=======
>>>>>>> Stashed changes
#finnish
if __name__ == '__main__':
    app.run(debug=True)


