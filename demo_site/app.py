import traceback
from flask import Flask, render_template, redirect, url_for, request, make_response
import requests
from cookies import cookies

config = {
    "DEBUG": True,  # some Flask specific configs
}


app = Flask(__name__)

cookie = cookies()

@app.route("/users/login", methods=['GET',"POST"])
def login():
    
     error = None
    
     if request.method == 'POST':
         
        cookie_check = cookie.check_for_cookie()
         
        if cookie_check:
            return cookie_check #How to redirect to some other endpoint with username?

        response = requests.get(f"http://127.0.0.1:8080/user_login/{request.form['u']}/{request.form['p']}")
        
        res = response.json()
        
        if res['error'] == False:
            
            response = make_response(res['message'])
            
            return response
            
        else:
            error = res['message']
            
     
     return render_template('login.html', error = error)


@app.route("/users/signup", methods=['GET',"POST"])
def sign_up():
    
     error = None
    
     if request.method == 'POST':
         
        cookie_check = cookie.check_for_cookie()
         
        if cookie_check:
            return cookie_check #How to redirect to some other endpoint with username?
     
        response = requests.get(f"http://127.0.0.1:8080/user_signup/{request.form['firstname']}/{request.form['lastname']}/{request.form['u']}/{request.form['p']}")
        
        res = response.json()
        
        if res['error'] == False:
            return res['message']
        else:
            error = res['message']
     
     return render_template('signup.html', error = error)
    

# Cookie checker
@app.route('/getcookie')
def getcookie():
   name = request.cookies.get('session')
   
   print(name)
   
   return '<h1>welcome ' + name + '</h1>'   

app.run(host='0.0.0.0', port=2520)


# todo

# For every signed up user, there should be a GUID to keep track