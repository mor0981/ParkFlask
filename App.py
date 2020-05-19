from flask import Flask,render_template,request,flash,session,redirect,url_for,abort
from forms import LoginForm,SignOutForm,NewParkForm,DeleteParkForm,signupForm,signout2Form,commentForm,PostForm
from datetime import datetime
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

commentNum=0

@app.route('/delete_comment',methods=['GET', 'POST'])
def delete_comment():
    form=commentForm()
    if form.validate_on_submit():
        docs=db.collection(u'Comments').stream()
        date=form.date.data
        time=form.time.data
        park=form.parkname.data
        for doc in docs:
            d=doc.to_dict()

            if date==d['date'] and time==d['time'] and park==d['parkname']:

                db.collection(u'Comments').document(doc.id).delete()
                return redirect(url_for("homePage"))

    return render_template('delete_comment.html',form=form)



@app.route('/comment',methods=['GET', 'POST'])
def comment():
    global commentNum
    commentNum=commentNum+1
    form=commentForm()
    if form.validate_on_submit():
        print("hi")
        now = datetime.now()
        date=now.strftime("%d/%m/%Y")
        time=now.strftime("%H:%M:%S")
        print(date)
        print(time)
        email=form.email.data
        password=form.password.data
        parkName=form.parkname.data
        docs=db.collection(u'Users').stream()
        for doc in docs:
            d=doc.to_dict()

            if email==d['email'] and password==d['password']:
                data={'email':email,'password':password, 'comment':form.comment.data,'time':time,'date':date,'parkName':parkname}
                print(data)
                db.collection(u'Comments').document().set(data)
                print(form.comment.data)
                print(commentNum)
                print(date)
                print(time)
                return redirect(url_for("homePage"))
                break

    print(form.email.data)
    print("hiyou")
    return render_template('comment.html',form=form)





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

@app.route('/review/<p>',methods=['GET', 'POST'])
def review(p):
        return render_template('comments.html',admin=session["admin"],parkName=p)


@app.route('/elements',methods=['GET', 'POST'])
def elements():
        return render_template('elements.html',data=data)


x=0
def idcount():
    global x
    x += 1
    return x/2



@app.route("/comment/<int:post_id>")
def Comment_guest(post_id):
    #post=db.collection(u'testComments').query.get_or_404(post_id)
    post=db.collection(u'testComments').where(u'post_id',u'==',1).stream()

   # rpost=post.to_dict()['title']
    docs = db.collection(u'testComments').stream()
    canMakePark = True
    print(post_id)
    for doc in docs:
        dici = doc.to_dict()
        if  dici['post_id']==post_id :
            canMakePark = False
            rpost=dici['title']
            wanted=dici
    if canMakePark==True:
        flash("error!")
        rpost='title'
        wanted=dici
    else:
        rpost=wanted['title']

 
    print(post)
    #post = Post.query.get_or_404(post_id)
    return render_template('updatePark.html', title=rpost, post=wanted)


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
    ref_my=ref_comment.where(u'post_id',u'==',1).stream()
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
        ref_my=ref_comment.where(u'post_id',u'==',1).get()
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


#finnish
if __name__ == '__main__':
    app.run(debug=True)
