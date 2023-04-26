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
    # Display the login page (GET request)
    @app.route("/users/login", methods=["GET"])
    def show_login_page():
        try:
            error = None
            # Check if the user is already logged in (valid cookie)
            cookie_validity, is_cookie_valid, user_id = cookie_service.check_cookie()
            
            if is_cookie_valid:
                # Redirect to the index page if the user is already logged in
                return redirect(url_for("index"))

            # Render the login page if the user is not logged in
            return render_template("login.html", error=error)
        except Exception as e:
            print(traceback.format_exc())
            return render_template("error.html", error=str(e))

    # Process the login form (POST request)
    @app.route("/users/login", methods=["POST"])
    def login():
        try:
            # Get the user login data from the form
            user_login = LoginPostModel(request.form["u"], request.form["p"])
            # Attempt to log the user in
            res = login_service.user_login(user_login)

            if res["error"]:
                # Display an error message if the login failed
                return render_template("login.html", error=res["error"])

            # Set the cookie and redirect to the index page if the login succeeded
            login_response_data = LoginResponseModel(res)
            
            return cookie_service.return_cookie(login_response_data)
        
        except Exception as e:
            print(traceback.format_exc())
            return render_template("error.html", error=str(e))

    # Display the signup page (GET request)
    @app.route("/users/signup", methods=["GET"])
    def show_signup_page():
        try:
            error = None
            
            return render_template("signup.html", error=error)
        
        except Exception as e:
            print(traceback.format_exc())
            return render_template("error.html", error=str(e))

    # Process the signup form (POST request)
    @app.route("/users/signup", methods=["POST"])
    def sign_up():
        try:
            # Get the user signup data from the form
            user_signup_data = SignupPostModel(
                request.form["firstname"],
                request.form["lastname"],
                request.form["u"],
                request.form["p"],
            )
            # Attempt to create a new user
            res = signup_service.create_user(user_signup_data)
            
            print(res)

            if res["error"]:
                # Display an error message if the signup failed
                return render_template("signup.html", error=res["error"])

            # Set the cookie and redirect to the index page if the signup succeeded
            signup_response_data = SignupResponseModel(res)
            
            return cookie_service.return_cookie(signup_response_data)
        
        except Exception as e:
            print(traceback.format_exc())
            return render_template("error.html", error=str(e))
