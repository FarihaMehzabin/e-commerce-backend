import traceback, json
from flask import Flask, render_template, request, jsonify, redirect, url_for
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

    user_logged, user_not_logged, user_id = cookie.check_cookie()
    
    products = requests.get(
            f"http://127.0.0.1:8080/pull-all-products"
        )
    
    products_json = products.json()

    return render_template("home.html", data = products_json['products']['products'],user_not_logged = user_not_logged, user_logged = user_logged, user_id = user_id)


@app.route("/checkout", methods=["GET"])
def show_checkout_page():
    
    return render_template("checkout.html")


@app.route("/proceed-to-payment", methods=["POST"])
def proceed_to_payment():
    checkout_data = request.get_json()
    
    user_logged, user_not_logged, user_id = cookie.check_cookie()
    
    checkout_data["user_id"] = user_id
    
    response = requests.post(
            f"http://127.0.0.1:8080/process-orders", 
            json = checkout_data
        )
    
    if response.json()['order_created']:
        return jsonify({"redirect_url": url_for("payment")}), 201
    
    return jsonify({"message": response.json()['message']})
    

@app.route("/payment", methods=["GET"])
def payment():
    return render_template("payment.html")



app.run(host="0.0.0.0", port=2520)




