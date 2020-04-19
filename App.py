from flask import Flask,render_template,request,flash,session,redirect,url_for
from forms import LoginForm,SignOutForm,registerForm,testForm
import pyrebase
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



"""hello"""
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
    form=registerForm()

    return render_template('basic.html',form=form)
"""unregister"""
@app.route('/unregister',methods=['GET', 'POST'])
def unregister():
    return render_template('basic3.html')
@app.route('/test',methods=['GET', 'POST'])
def test():
    form=testForm()
    form1=testForm(request.form)
    name=form1.email.data
    password=form1.password.data
    print(name)
    auth.create_user_with_email_and_password(name,password)
    return  redirect(url_for("user"))
    """
    if form.validate_on_submit():
        try:
            auth.create_user_with_email_and_password(form.email.data,form.password.data)
            print("in try")
            return render_template(url_for("user"))
        except:
            print("in except")
            return render_template("testing.html",form=form)

    print("in else")
    return render_template("testing.html",form=form)
"""


"""finnish"""
if __name__ == '__main__':
    app.run(debug=True)
