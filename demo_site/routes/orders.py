import traceback
from flask import request, jsonify, render_template,url_for
import requests
from services.cookies import Cookies



cookie = Cookies()


def order_routes(app):
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


