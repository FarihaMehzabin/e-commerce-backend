from email import message
import traceback
from unicodedata import category
from flask import Flask, render_template, redirect, url_for, request, jsonify
import requests
from cookies import cookies
from models.post_data_models.signup import SignupPostModel
from models.post_data_models.login import LoginPostModel
from models.response_models.signup import SignupResponseModel
from services.signup import SignupService
from services.login import LoginService

config = {
    "DEBUG": True,  # some Flask specific configs
}


app = Flask(__name__)

cookie = cookies()
signup_service = SignupService()



@app.route("/")
def index():
    
    user_logged, user_not_logged = cookie.check_cookie()
    
    return render_template("home.html", user_not_logged = user_not_logged, user_logged = user_logged)


@app.route('/manage-categories')
def manage_categories():
    
    category_list_response = requests.get(
            f"http://127.0.0.1:8080/get-all-category"
        )
    
    category_list = category_list_response.json()
    
    return render_template("manage_categories.html", categories = category_list["category_list"])


@app.route("/company/user/login", methods=["GET", "POST"])
def login():

    error = None
    
    check_cookie = cookie.check_cookie_with_redirect('index')

    if check_cookie is not False:
        return check_cookie


    if request.method == "POST":
        
        user_login = LoginPostModel(request.form['u'], request.form['p'])
        

        response = requests.get(
            f"http://127.0.0.1:8080/company/user/login/{request.form['u']}/{request.form['p']}"
        )

        res = response.json()

        print(res)
        
        # no error found 
        if res["error"] == False:

            set_cookie = cookie.set_cookie(res["comp_id"])

            set_cookie.headers["location"] = url_for("index")

            return set_cookie, 302

        else:
            error = res["message"]

    return render_template("login.html", error=error)


@app.route("/company/user/signup", methods=["GET", "POST"])
def sign_up():

    error = None

    if request.method == "POST":
        
        user_signup = SignupPostModel(request.form['cname'], request.form['u'], request.form['p'] )
        
        res = signup_service.create_user(user_signup)
        
        signup_data = SignupResponseModel(res['message'], res['error'], res['comp_id'])
        
        # no error message
        if signup_data.error == False:
            set_cookie = cookie.set_cookie(res["comp_id"])

            set_cookie.headers["location"] = url_for("index")

            return set_cookie, 302
        else:
            error = res["message"]

    return render_template("signup.html", error=error)



# todo Product category manage (create/edit/delete)

# View product list to edit
# Choose a product to change the category
# View product with the current category and list of categories available
# can create a new category
# can edit a category
# can delete a category

# creating categories 
@app.route("/product/manage-category/create", methods=["GET", "POST"])
def create_category():

    # Get the JSON data from the request
    data = request.get_json()

    # Extract the category name from the JSON data from frontend
    category_name = data['category_name']
    
    # add to category table
    response = requests.get(
            f"http://127.0.0.1:8080/company/add-category/{category_name}"
        )
    
    # get category id from the response
    res = response.json()
    
    # Return a response indicating success
    return jsonify({'message': res['message']}), 201
    

# Editing existing category
@app.route("/product/manage-category/edit", methods=["GET", "POST"])
def edit_category():

    # Get the JSON data from the request
    data = request.get_json()

    category_name = data['category_name']
    new_category_name = data['new_category_name']

    
    response = requests.post(
        "http://127.0.0.1:8080/company/edit-category/",
        json={"category_name": category_name, "new_category_name": new_category_name},
    )
    
    res = response.json()
    
    # Return a response indicating success
    return jsonify({'message': res['message']}), 201

# Deleting existing category
@app.route("/product/manage-category/delete", methods=["GET", "POST"])
def delete_category():

    # Get the JSON data from the request
    data = request.get_json()

    category_name = data['category_name']

    # Change the URL to match your API
    response = requests.post(
        "http://127.0.0.1:8080/company/delete-category/",
        json={"category_name": category_name},
    )
    # get category id from the response
    res = response.json()
    
    # Return a response indicating success
    return jsonify({'message': res['message']}), 201


app.run(host="0.0.0.0", port=1234)
