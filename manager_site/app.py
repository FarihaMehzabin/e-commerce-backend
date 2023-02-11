import traceback
from flask import Flask, render_template, redirect, url_for, request
import requests
from cookies import cookies

config = {
    "DEBUG": True,  # some Flask specific configs
}


app = Flask(__name__)

cookie = cookies()
    

@app.route("/company_user/login", methods=['GET',"POST"])
def login():
    
     error = None
    
     if request.method == 'POST':
         
        cookie_check = cookie.check_for_cookie()
         
        if cookie_check:
            return cookie_check #How to redirect to some other endpoint with username?
     
        response = requests.get(f"http://127.0.0.1:8080/company_login/{request.form['u']}/{request.form['p']}")
        
        res = response.json()
     
        if res['error'] == False:
            return res['message']
        else:
            error = res['message']
     
     return render_template('login.html', error = error)
     

@app.route("/company_user/signup", methods=['GET',"POST"])
def sign_up():
    
     error = None
    
     if request.method == 'POST':
         
        cookie_check = cookie.check_for_cookie()
         
        if cookie_check:
            
            return cookie_check
     
        response = requests.get(f"http://127.0.0.1:8080/company_signup/{request.form['cname']}/{request.form['u']}/{request.form['p']}")
        
        res = response.json()
        
        if res['error'] == False:
            return res['message']
        else:
            error = res['message']
     
     return render_template('signup.html', error = error)
    
    
    

app.run(host='0.0.0.0', port=1234)