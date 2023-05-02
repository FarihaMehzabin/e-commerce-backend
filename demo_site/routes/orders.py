import traceback
from flask import request, jsonify, render_template,url_for, redirect
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
        
        response_json = response.json()
        
        if response_json['order_created']:
            
            return_url = "http://localhost:2520/payment-return"

            payment_url = f"http://localhost:8010?user_id={user_id}&total={response_json['total']}&currency=USD&return={return_url}"

            return jsonify({"redirect_url": payment_url}), 201
        
        return jsonify({"message": response.json()['message']})
        
  
    @app.route("/payment-return", methods=["GET"])
    def payment_return():
        transaction_id = request.args.get("transaction")
        user_id = request.args.get("user_id")
        transaction_status_url = f"http://localhost:8010/transaction-status?transaction={transaction_id}"
        
        print(transaction_status_url)

        # Call the transaction_status endpoint to verify the transaction
        response = requests.get(transaction_status_url)
        transaction_data = response.json()
        
        print(transaction_data)

        if transaction_data["result"] == "success":
            # Update the database with the transaction details and unlock reserved stock rows
            reservation_response = requests.get(f"http://127.0.0.1:8080/delete-reservations?user_id={user_id}")
            
            reservation_response_json = reservation_response.json()
            
            if reservation_response_json["success"]:
                return redirect("/payment-success", code=302)
            
            return redirect(url_for('refund_page', message = reservation_response_json['message']))
        else:
            return redirect("/payment-error", code=302)


    @app.route("/payment-success", methods=["GET"])
    def payment_success():
        return "Hey, your payment worked, your order is placed, thanks!"


    @app.route("/payment-error", methods=["GET"])
    def payment_error():
        return "Sorry, there was an error with your payment."
    
    
    @app.route("/product-stock-out", methods=["GET"])
    def refund_page():
        message = requests.args.get("message")
        
        return message
        


