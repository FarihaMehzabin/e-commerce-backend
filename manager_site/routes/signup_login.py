import traceback
from flask import (
    request,
    render_template,
    url_for,
    redirect,
)
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
        try:
            error = None
            cookie_validity, is_cookie_valid = cookie_service.check_cookie()
            if is_cookie_valid:
                return redirect(url_for("index"))
            return render_template("login.html", error=error)
        except Exception as e:
            print(traceback.format_exc())
            return render_template("error.html", error=str(e))

    @app.route("/company/user/login/submit", methods=["POST"])
    def process_login():
        try:
            user_login = LoginPostModel(request.form["u"], request.form["p"])
            res = login_service.user_login(user_login)

            if res["error"]:
                return render_template("login.html", error=res["error"])

            login_response_data = LoginResponseModel(res)
            return cookie_service.return_cookie(login_response_data)
        except Exception as e:
            print(traceback.format_exc())
            return render_template("error.html", error=str(e))

    @app.route("/company/user/signup", methods=["GET"])
    def signup():
        try:
            return render_template("signup.html", error=None)
        except Exception as e:
            print(traceback.format_exc())
            return render_template("error.html", error=str(e))

    @app.route("/company/user/signup-submit", methods=["POST"])
    def signup_submit():
        try:
            user_signup_data = SignupPostModel(
                request.form["cname"], request.form["u"], request.form["p"], request.form["email"]
            )
            res = signup_service.create_user(user_signup_data)

            if res["error"]:
                return render_template("signup.html", error=res["error"])

            signup_response_data = SignupResponseModel(res)
            return cookie_service.return_cookie(signup_response_data)
        except Exception as e:
            print(traceback.format_exc())
            return render_template("error.html", error=str(e))
