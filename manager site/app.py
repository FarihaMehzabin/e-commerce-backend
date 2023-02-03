import traceback
from flask import Flask, render_template, redirect, url_for, request
from db import Db



config = {
    "DEBUG": True,  # some Flask specific configs
}



app = Flask(__name__)

db = Db()


@app.route("/users/login", methods=['GET',"POST"])
def login():
    error = None
    if request.method == 'POST':
        
        user = db.user_login(request.form['u'], request.form['p'])
        
        if user:
            # return redirect(url_for('home'))
            return f"Logged in! Welcome, {request.form['u']} :)"
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route("/users/signup", methods=['GET',"POST"])
def sign_up():
    error = None
    if request.method == 'POST':
        
        user = db.user_signup(request.form['firstname'], request.form['lastname'],request.form['u'], request.form['p'])
        
        print(user)
        
        if user:
            # return redirect(url_for('home'))
            return f"New user signed up! Welcome, {request.form['u']} :)"
        else:
            error = 'Username taken. Please try again.'
    return render_template('signup.html', error=error)

app.run(host='0.0.0.0', port=1234)