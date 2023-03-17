import traceback
from hashing import Hashing
from views import Views
from flask import Flask, render_template, redirect, url_for, request, jsonify
from db import Db
import uuid
from categories import Category


config = {
    "DEBUG": True,  # some Flask specific configs
}

app = Flask(__name__)


views = Views()
db = Db()
hash = Hashing()
category = Category()

# returns report on total value spent by each user
@app.route("/users/total-value-spent", methods=["GET"])
def total_val_spent():
    try:
        return views.total_value_spent()
    
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")

# returns top purchased products from the database
@app.route("/users/top-purchased-product", methods=["GET"])
def top_purchased_product():
    try:
        return views.top_purchased_product()
     
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")


# returns top 10 users who purchased the highest amount of products
@app.route("/users/top-10-user", methods=["GET"])
def top_10_user():
    try:
        return views.top_10_user()
    
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")
 
 
#  Public users login
@app.route("/user-login/<username>/<password>", methods=['GET'])
def login(username, password):
    
        user, user_id  = db.user_login(username,password)
        if user:
            return jsonify(message = f"Logged in! Welcome, {username} :)", error= False, u_id = user_id)
        else:
            return jsonify(message = 'Invalid Credentials. Please try again.', error = True)
            

# Public user signup
@app.route("/user-signup/<fname>/<lname>/<username>/<password>", methods=['GET'])
def sign_up(fname, lname, username, password):
        
        user, user_id = db.user_signup(fname, lname, username, password)
        
        if user:
            return jsonify(message = f"New user signed up! Welcome, {username} :)", error= False, u_id = user_id)
        else:
            return jsonify(message = 'Username taken. Please try again.', error = True)


       
# company users signup
@app.route("/company/user/signup/<cname>/<username>/<password>", methods=['GET'])
def comp_sign_up(cname, username, password):
        
        user, company_id = db.comp_signup(cname, username, password)
        
        if user:
            return jsonify(message = f"New user signed up! Welcome, {username} :)", error= False, comp_id = company_id)
        else:
            return jsonify(message = 'Username taken. Please try again.', error = True, comp_id = 0)


# company users login
@app.route("/company/user/login/<username>/<password>", methods=['GET'])
def comp_login(username, password):
    
        user, company_id = db.comp_login(username,password)
        
        print(user)
        
        if user:
            return jsonify(message = f"Logged in! Welcome, {username} :)", error= False, comp_id = company_id)
        else:
            return jsonify(message = 'Invalid Credentials. Please try again.', error = True)


# creates a session for the company users
# generates a GUID, hash it and adds it along with the company id to the 
# session table
@app.route("/company/create-session/<comp_id>", methods = ["GET"])
def create_session_comp(comp_id):
    
    guid_id = str(uuid.uuid4())
    
    hashed_guid = hash.hash_guid(guid_id)
    
    db.add_to_session_comp(hashed_guid, comp_id)
    
    return jsonify( guid = hashed_guid )


# creates a session for the public users
# generates a GUID, hash it and adds it along with the user id to the 
# session table
@app.route("/user/create-session/<user_id>", methods = ["GET"])
def create_session_user(user_id):
    
    guid_id = str(uuid.uuid4())
    
    hashed_guid = hash.hash_guid(guid_id)
    
    db.add_to_session_user(hashed_guid, user_id)
    
    return jsonify( guid = hashed_guid )


# check is the cookie sent by the client for login is valid. This endpoint is 
# for the company users only. It returns a booolean to indicate whether 
# the cookie is valid and the name of the company
@app.route("/company/check-cookie-validity/<guid>", methods=['GET',"POST"])
def check_cookie_validity_comp(guid):
    try:
        is_session_valid, company = db.check_session_comp(guid)
        
        return jsonify(check = is_session_valid, comp = company)
    
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")
        
# check is the cookie sent by the client for login is valid. This endpoint is 
# for the public users only. It returns a booolean to indicate whether 
# the cookie is valid and the name of the user
@app.route("/user/check-cookie-validity/<guid>", methods=['GET',"POST"])
def check_cookie_validity_user(guid):
    try:
        is_session_valid, u = db.check_session_user(guid)
        
        return jsonify(check = is_session_valid, user = u)
    
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")
        
#  Pull registered products to the home page of public users
@app.route("/company/pull-products", methods=['GET'])
def pull_products_for_company():
    try:
        products = db.get_products()
        
        return jsonify(products = products)
    
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")
        

# add a new category to category table
# data sent to db: category name
# data received from db: category_id
@app.route("/company/add-category/<category_name>", methods=['GET'])
def add_category(category_name):
    try:
        category_id = category.add_category(category_name)
        
        return jsonify(message = "new category added")
    
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")

# edit existing category in the category table
# returns edited category name 
@app.route("/company/edit-category/", methods=['POST'])
def edit_category():
    try:
        
        data = request.get_json()
        
        category_name = data['category_name']
        
        new_category_name = data['new_category_name']
        
        message = category.edit_category(category_name, new_category_name)
        
        return jsonify(message = message)
    
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")
        

# delete existing category
@app.route("/company/delete-category/", methods=['POST'])
def delete_category():
    try:
        
        data = request.get_json()
        
        category_name = data['category_name']
        
        category_id = category.delete_category(category_name)
        
        return jsonify(message = "category deleted successfully")
    
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")
        

@app.route('/get-all-category', methods=['GET'])
def get_all_category():
    
    category_list = category.category_list()
    
    return jsonify(category_list = category_list)

      
app.run(host='0.0.0.0', port=8080)