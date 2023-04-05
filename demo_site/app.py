import traceback
from flask import Flask, render_template
import requests

from routes.signup_login import signup_login_routes
from services.cookies import Cookies

config = {
    "DEBUG": True,  # some Flask specific configs
}


app = Flask(__name__)

signup_login_routes(app)

cookie = Cookies()

@app.route("/")
def index():

    user_logged, error = cookie.check_cookie()
    
    products = requests.get(
            f"http://127.0.0.1:8080/company/pull-products"
        )
    
    products_json = products.json()
    
    print(products_json['products'])
    
    return render_template("home.html", data = products_json['products'], message = user_logged)


app.run(host="0.0.0.0", port=2520)

