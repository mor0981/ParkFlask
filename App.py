from flask import Flask,render_template,request
from forms import LoginForm
app = Flask(__name__)
app.config['SECRET_KEY']='mormormor'

@app.route('/',methods=['GET', 'POST'])
@app.route('/home',methods=['GET', 'POST'])
def home():
    form = LoginForm()
    print("dddddddddddddddddddddddddddddddd")
    print(form.email.data)
    return render_template('index.html',form=form)

@app.route('/about')
def about():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)