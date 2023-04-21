from email import message
import traceback
from unicodedata import category
from services.cookies import Cookies
from flask import Flask, render_template, redirect, url_for, request, jsonify
from routes.signup_login import signup_login_routes
from routes.category import category_routes
from manager_site.routes.products import products_routes


config = {
    "DEBUG": True,  # some Flask specific configs
}


app = Flask(__name__)

signup_login_routes(app)
category_routes(app)
products_routes(app)

cookie = Cookies()



@app.route("/")
def index():
    
    user_logged, user_not_logged, company_id = cookie.check_cookie()
    
    return render_template("home.html", user_not_logged = user_not_logged, user_logged = user_logged, company_id = company_id)


app.run(host="0.0.0.0", port=1234)
