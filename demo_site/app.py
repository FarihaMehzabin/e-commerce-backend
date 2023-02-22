import traceback
from flask import Flask, render_template, redirect, url_for, request, make_response
import requests
from cookies import cookies

config = {
    "DEBUG": True,  # some Flask specific configs
}


app = Flask(__name__)

cookie = cookies()


@app.route("/")
def index():

    user_logged = cookie.check_cookie()
    
    products = requests.get(
            f"http://127.0.0.1:8080/company/pull-products"
        )
    
    products_json = products.json()
    
    print(products_json['products'])
    
    return render_template("home.html", data = products_json['products'], message = user_logged)



@app.route("/users/login", methods=["GET", "POST"])
def login():

    error = None

    check_cookie = cookie.check_cookie_with_redirect("index")

    if check_cookie is not False:
        return check_cookie

    if request.method == "POST":

        response = requests.get(
            f"http://127.0.0.1:8080/user-login/{request.form['u']}/{request.form['p']}"
        )

        res = response.json()

        if res["error"] == False:

            set_cookie = cookie.set_cookie(res["u_id"])

            set_cookie.headers["location"] = url_for("index")

            return set_cookie, 302

        else:
            error = res["message"]

    return render_template("login.html", error=error)


@app.route("/users/signup", methods=["GET","POST"])
def sign_up():

    error = None

    if request.method == "POST":

        response = requests.get(
            f"http://127.0.0.1:8080/user-signup/{request.form['firstname']}/{request.form['lastname']}/{request.form['u']}/{request.form['p']}"
        )

        res = response.json()

        if res["error"] == False:
            set_cookie = cookie.set_cookie(res["u_id"])

            set_cookie.headers["location"] = url_for("index")

            return set_cookie, 302
        else:
            error = res["message"]

    return render_template("signup.html", error=error)


# Cookie checker
@app.route("/getcookie")
def getcookie():
    name = request.cookies.get("session")

    print(name)

    return "<h1>welcome " + name + "</h1>"


app.run(host="0.0.0.0", port=2520)


# todo

# For every signed up user, there should be a GUID to keep track?
