from distutils.log import error
from email import message
import traceback
from hashing import Hashing
from views import Views
from flask import Flask, render_template, redirect, url_for, request, jsonify
from db import Db
import uuid


config = {
    "DEBUG": True,  # some Flask specific configs
}

app = Flask(__name__)


views = Views()
db = Db()
hash = Hashing()

# Reports
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
 
 
# Public users signup/login
@app.route("/user_login/<username>/<password>", methods=['GET',"POST"])
def login(username, password):
    
        user = db.user_login(username,password)
        if user:
            return jsonify(message = f"Logged in! Welcome, {username} :)", error= False)
        else:
            return jsonify(message = 'Invalid Credentials. Please try again.', error = True)
            

@app.route("/user_signup/<fname>/<lname>/<username>/<password>", methods=['GET',"POST"])
def sign_up(fname, lname, username, password):
        
        user = db.user_signup(fname, lname, username, password)
        
        if user:
            return jsonify(message = f"New user signed up! Welcome, {username} :)", error= False)
        else:
            return jsonify(message = 'Username taken. Please try again.', error = True)


       
# company users signup/login
@app.route("/company_signup/<cname>/<username>/<password>", methods=['GET',"POST"])
def comp_sign_up(cname, username, password):
        
        user = db.comp_signup(cname, username, password)
        
        if user:
            return jsonify(message = f"New user signed up! Welcome, {username} :)", error= False)
        else:
            return jsonify(message = 'Username taken. Please try again.', error = True)

@app.route("/company_login/<username>/<password>", methods=['GET',"POST"])
def comp_login(username, password):
    
        user = db.comp_login(username,password)
        
        if user:
            return jsonify(message = f"Logged in! Welcome, {username} :)", error= False)
        else:
            return jsonify(message = 'Invalid Credentials. Please try again.', error = True)


# Cookie setup
@app.route("/generate_and_store_GUID")
def generate_and_store_GUID():
    
    guid_id = str(uuid.uuid4())
    
    hashed_guid = hash.hash_guid(guid_id)
    
    db.add_to_session(hashed_guid)
    
    return jsonify( guid = hashed_guid )

@app.route("/check_cookie_validity/<guid>", methods=['GET',"POST"])
def check_cookie_validity(guid):
    try:
        is_session_valid = db.check_session(guid)
        
        return jsonify(check = is_session_valid)
    
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")

app.run(host='0.0.0.0', port=8080)