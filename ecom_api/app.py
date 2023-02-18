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
@app.route("/users/total-value-spent", methods=["GET"])
def total_val_spent():
    try:
        return views.total_value_spent()
    
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")

@app.route("/users/top-purchased-product", methods=["GET"])
def top_purchased_product():
    try:
        return views.top_purchased_product()
     
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")

@app.route("/users/top-10-user", methods=["GET"])
def top_10_user():
    try:
        return views.top_10_user()
    
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")
 
 
# Public users signup/login
@app.route("/user-login/<username>/<password>", methods=['GET'])
def login(username, password):
    
        user = db.user_login(username,password)
        if user:
            return jsonify(message = f"Logged in! Welcome, {username} :)", error= False)
        else:
            return jsonify(message = 'Invalid Credentials. Please try again.', error = True)
            

@app.route("/user-signup/<fname>/<lname>/<username>/<password>", methods=['GET'])
def sign_up(fname, lname, username, password):
        
        user = db.user_signup(fname, lname, username, password)
        
        if user:
            return jsonify(message = f"New user signed up! Welcome, {username} :)", error= False)
        else:
            return jsonify(message = 'Username taken. Please try again.', error = True)


       
# company users signup/login
@app.route("/company/user/signup/<cname>/<username>/<password>", methods=['GET'])
def comp_sign_up(cname, username, password):
        
        user, company_id = db.comp_signup(cname, username, password)
        
        if user:
            return jsonify(message = f"New user signed up! Welcome, {username} :)", error= False, comp_id = company_id)
        else:
            return jsonify(message = 'Username taken. Please try again.', error = True)

@app.route("/company/user/login/<username>/<password>", methods=['GET'])
def comp_login(username, password):
    
        user, company_id = db.comp_login(username,password)
        
        print(user)
        
        if user:
            return jsonify(message = f"Logged in! Welcome, {username} :)", error= False, comp_id = company_id)
        else:
            return jsonify(message = 'Invalid Credentials. Please try again.', error = True)


# Cookie setup
@app.route("/create-session/<comp_id>", methods = ["GET"])
def create_session(comp_id):
    
    guid_id = str(uuid.uuid4())
    
    hashed_guid = hash.hash_guid(guid_id)
    
    db.add_to_session(hashed_guid, comp_id)
    
    return jsonify( guid = hashed_guid )

@app.route("/check-cookie-validity/<guid>", methods=['GET',"POST"])
def check_cookie_validity(guid):
    try:
        is_session_valid, company = db.check_session(guid)
        
        return jsonify(check = is_session_valid, comp = company)
    
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")

app.run(host='0.0.0.0', port=8080)