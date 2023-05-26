from flask import url_for
import requests
from logger import Logger

class OrderService:
    def __init__(self):
        self.logger = Logger()

    def create_order(self, checkout_data):
        try:
            self.logger.info("Starting create_order method")

            response = requests.post(
                f"http://127.0.0.1:8080/create-order", 
                json = checkout_data
            )
            response_json = response.json()

            if response_json['order_created']:
                return_url = f"http://localhost:2520/payment-return?order_id={response_json['order_id']}"
                
                payment_url = f"http://localhost:8010?user_id={checkout_data['user_id']}&total={response_json['total']}&currency=USD&return={return_url}"
                
                self.logger.info("Order creation successful, redirecting to payment")
                
                return True, {"redirect_url": payment_url}
            
            self.logger.error("Error during order creation: %s", response_json['message'])
            
            return False, {"message": response_json['message']}
        
        except Exception as e:
            self.logger.error("Exception in create_order: %s", str(e))
            return False, {"message": "Error in creating order"}

    def payment_return(self, transaction_status_url, user_id, order_id):
        try:
            self.logger.info("Starting payment_return method")

            response = requests.get(transaction_status_url)
            
            transaction_data = response.json()

            if transaction_data["result"] == "success":
                
                reservation_response = requests.get(f"http://127.0.0.1:8080/process-paid-orders?user_id={user_id}&order_id={order_id}")
                
                reservation_response_json = reservation_response.json()

                if reservation_response_json["success"]:
                
                    self.logger.info("Payment success, redirecting")
                
                    return "/payment-success", 302
                
                self.logger.error("Error in processing order: %s", reservation_response_json['message'])
                
                return url_for('refund_page', message = reservation_response_json['message']), 302
            else:
                self.logger.error("Payment failed")
                return "/payment-error", 302
        
        except Exception as e:
            self.logger.error("Exception in payment_return: %s", str(e))
            return "/payment-error", 302
