from distutils.log import error
from email import message
import traceback
from views import Views
from flask import Flask, render_template, redirect, url_for, request, jsonify
from db import Db



config = {
    "DEBUG": True,  # some Flask specific configs
}



app = Flask(__name__)


views = Views()
db = Db()

@app.route("/users/total_value_spent", methods=["GET"])
def total_val_spent():
    try:
        return views.total_value_spent()
    
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")

@app.route("/users/top_purchased_product", methods=["GET"])
def top_purchased_product():
    try:
        return views.top_purchased_product()
     
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")

@app.route("/users/top_10_user", methods=["GET"])
def top_10_user():
    try:
        return views.top_10_user()
    
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")
        
@app.route("/users/<username>/<password>", methods=['GET',"POST"])
def login(username, password):
    
        user = db.user_login(username,password)
        
        if user:
            return jsonify(message = f"Logged in! Welcome, {username} :)", error= False)
        else:
            return jsonify(message = 'Invalid Credentials. Please try again.', error = True)
            

@app.route("/users/<fname>/<lname>/<username>/<password>", methods=['GET',"POST"])
def sign_up(fname, lname, username, password):
        
        user = db.user_signup(fname, lname, username, password)
        
        if user:
            return jsonify(message = f"New user signed up! Welcome, {username} :)", error= False)
        else:
            return jsonify(message = 'Username taken. Please try again.', error = True)
        

app.run(host='0.0.0.0', port=8080)