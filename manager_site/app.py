from email import message
import traceback
from flask import Flask, render_template, redirect, url_for, request
import requests
from cookies import cookies

config = {
    "DEBUG": True,  # some Flask specific configs
}


app = Flask(__name__)

cookie = cookies()


@app.route("/")
def index():
    
    return cookie.check_cookie()
    
    return render_template("home.html", data = products_json['products'], message = user_logged)



@app.route("/company/user/login", methods=["GET", "POST"])
def login():

    error = None
    
    check_cookie = cookie.check_cookie_with_redirect('index')

    if check_cookie is not False:
        return check_cookie


    if request.method == "POST":

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

        response = requests.get(
            f"http://127.0.0.1:8080/company/user/signup/{request.form['cname']}/{request.form['u']}/{request.form['p']}"
        )

        res = response.json()
        
        # no error message
        if res["error"] == False:
            set_cookie = cookie.set_cookie(res["comp_id"])

            set_cookie.headers["location"] = url_for("index")

            return set_cookie, 302
        else:
            error = res["message"]

    return render_template("signup.html", error=error)


app.run(host="0.0.0.0", port=1234)
