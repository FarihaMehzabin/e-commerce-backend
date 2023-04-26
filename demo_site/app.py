import traceback, json
from flask import Flask, render_template, request, jsonify
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

@app.route("/checkout")
def checkout():
    
    return render_template("checkout.html")


@app.route("/submit_checkout", methods=["POST"])
def submit_checkout():
    checkout_data = request.get_json()

    items = checkout_data.get("items")
    delivery = checkout_data.get("delivery")
    
    print(items)
    
    print(delivery)

    # Process the checkout data and send it to the backend server
    # Add your code to process and send the data to the backend server

    # Return a response to the frontend
    return jsonify({"message": "Checkout data submitted successfully"})

app.run(host="0.0.0.0", port=2520)




