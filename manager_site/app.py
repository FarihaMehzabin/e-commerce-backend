import traceback
from flask import Flask, render_template, redirect, url_for, request
import requests

config = {
    "DEBUG": True,  # some Flask specific configs
}


app = Flask(__name__)


@app.route("/users/login", methods=['GET',"POST"])
def login():
    
     error = None
    
     if request.method == 'POST':
     
        response = requests.get(f"http://127.0.0.1:8080/users/{request.form['u']}/{request.form['p']}")
        
        res = response.json()
     
        if res['error'] == False:
            return res['message']
        else:
            error = res['message']
     
     return render_template('login.html', error = error)
     

@app.route("/users/signup", methods=['GET',"POST"])
def sign_up():
    
     error = None
    
     if request.method == 'POST':
     
        response = requests.get(f"http://127.0.0.1:8080/users/{request.form['firstname']}/{request.form['lastname']}/{request.form['u']}/{request.form['p']}")
        
        res = response.json()
        
        if res['error'] == False:
            return res['message']
        else:
            error = res['message']
     
     return render_template('signup.html', error = error)
    
    
    

app.run(host='0.0.0.0', port=1234)