from flask import Flask,render_template,request
from forms import LoginForm
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



@app.route('/',methods=['GET', 'POST'])
@app.route('/home',methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        print("ddddddddddddddd")
        try:
            auth.sign_in_with_email_and_password(form.email.data,form.password.data)
            return "Login"
        except:
            return "Not Exist"
    return render_template('index.html',form=form)

@app.route('/about')
def about():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)