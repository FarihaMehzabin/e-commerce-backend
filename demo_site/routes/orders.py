from flask import jsonify, render_template, url_for, redirect, request
import requests
from services.cookies import Cookies
from logger import Logger
from services.orders import OrderService

cookie = Cookies()
logger = Logger()

def order_routes(app):
    @app.route("/checkout", methods=["GET"])
    def show_checkout_page():
        try:
            return render_template("checkout.html")
        
        except Exception as e:
            logger.error("Error in show_checkout_page: {}".format(e))
            return jsonify({"message": "Server error"}), 500

    @app.route("/create-order", methods=["POST"])
    def proceed_to_payment():
        try:
            checkout_data = request.get_json()
            
            _, _, user_id = cookie.check_cookie()
                        
            checkout_data["user_id"] = user_id
                        
            order_service = OrderService()
            
            order_created, response = order_service.create_order(checkout_data)
            
            if order_created:
                return jsonify(response), 201
            
            return jsonify(response), 400
        
        except Exception as e:
            logger.error("Error in proceed_to_payment: {}".format(e))
            
            return jsonify({"message": "Server error"}), 500

    @app.route("/payment-return", methods=["GET"])
    def payment_return():
        try:
            transaction_id = request.args.get("transaction")
            user_id = request.args.get("user_id")
            order_id = request.args.get("order_id")
            
            transaction_status_url = f"http://localhost:8010/transaction-status?transaction={transaction_id}"
            
            order_service = OrderService()
            
            redirect_url, code = order_service.payment_return(transaction_status_url, user_id, order_id)
            
            return redirect(redirect_url, code=code)
        
        except Exception as e:
            logger.error("Error in payment_return: {}".format(e))
            return jsonify({"message": "Server error"}), 500

    
    @app.route("/payment-success", methods=["GET"])
    def payment_success():
        try:
            
            user_id = request.args.get("user_id")
            order_id = request.args.get("order_id")
            
            order_service = OrderService()
            
            success, response = order_service.process_delivery(user_id, order_id)
            
            if not success:
                logger.error("Error in payment_success: %s", response["message"])
                return jsonify({"message": "Server error"}), 500
                        
            return render_template('payment_success.html')
        
        except Exception as e:
            logger.error("Error in payment_success: {}".format(e))
            return jsonify({"message": "Server error"}), 500

    
    @app.route("/payment-error", methods=["GET"])
    def payment_error():
        try:
            
            return render_template('payment_error.html')
        
        except Exception as e:
            logger.error("Error in payment_error: {}".format(e))
            return jsonify({"message": "Server error"}), 500

    
    @app.route("/product-stock-out", methods=["GET"])
    def refund_page():
        try:
            
            return render_template('refund_page.html')
        
        except Exception as e:
            logger.error("Error in refund_page: {}".format(e))
            return jsonify({"message": "Server error"}), 500

