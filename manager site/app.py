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



app.run(host='0.0.0.0', port=1234)