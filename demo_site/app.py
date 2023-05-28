from email import message
import traceback, json
from flask import Flask, render_template
import requests

from routes.signup_login import signup_login_routes
from demo_site.routes.orders import order_routes
from services.cookies import Cookies

config = {
    "DEBUG": True,  # some Flask specific configs
}


app = Flask(__name__)

signup_login_routes(app)
order_routes(app)

cookie = Cookies()


@app.route("/")
def index():
    user_logged, message, user_id = cookie.check_cookie()

    print(user_logged, message, user_id)

    products = requests.get(f"http://127.0.0.1:8081/pull-all-products")

    products_json = products.json()

    return render_template(
        "home.html",
        data=products_json["products"]["products"],
        message=message,
        user_logged=user_logged,
        user_id=user_id,
    )


app.run(host="0.0.0.0", port=2520)
