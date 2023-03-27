import traceback
from flask import request, jsonify, json
import requests
from cookies import cookies
from models.post_data_models.signup import SignupPostModel
from models.post_data_models.login import LoginPostModel
from models.response_models.signup import SignupResponseModel
from services.signup import SignupService
from services.login import LoginService

def signup_login_routes(app):
    
    @app.route("/company/user/login", methods=["GET", "POST"])
    def login():

        error = None
        
        check_cookie = cookie.check_cookie_with_redirect('index')

        if check_cookie is not False:
            return check_cookie

        if request.method == "POST":
            
            user_login = LoginPostModel(request.form['u'], request.form['p'])
            
            payload = json.dumps(user_login.to_dict())

            response = requests.post(
                f"http://127.0.0.1:8080/company/user/login", 
                data=payload,
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