import traceback
from flask import request, jsonify, json, render_template, url_for, make_response, redirect
import requests
from services.cookies import Cookies
from models.post_data_models.signup import SignupPostModel
from models.post_data_models.login import LoginPostModel
from models.response_models.signup import SignupResponseModel
from models.response_models.login import LoginResponseModel
from services.signup import SignupService
from services.login import LoginService


cookie_service = Cookies()

signup_service = SignupService()
login_service = LoginService()


def signup_login_routes(app):
    
    @app.route("/company/user/login", methods=["GET"])
    def show_login_page():
        error = None
        
        cookie_validity, is_cookie_valid = cookie_service.check_cookie()
        
        if is_cookie_valid:
            return redirect(url_for("index"))

        return render_template("login.html", error=error)

    
    @app.route("/company/user/login/submit", methods=["POST"])
    def process_login():

        user_login = LoginPostModel(request.form['u'], request.form['p'])
        
        res = login_service.user_login(user_login)

        if res["error"]:
            return render_template("login.html", error=res["error"])

        login_response_data = LoginResponseModel(res)
        
        return cookie_service.return_cookie(login_response_data)
    

    @app.route("/company/user/signup", methods=["GET"])
    def sign_up():
        return render_template("signup.html", error=None)


    @app.route("/company/user/signup-submit", methods=["POST"])
    def signup_submit():
        user_signup_data = SignupPostModel(request.form['cname'], request.form['u'], request.form['p'])
        
        res = signup_service.create_user(user_signup_data)

        if res['error']:
            return render_template("signup.html", error=res['error'])

        signup_response_data = SignupResponseModel(res)
        
        return cookie_service.return_cookie(signup_response_data)
