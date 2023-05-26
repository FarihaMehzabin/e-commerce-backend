import traceback
from flask import request, jsonify
from flask_api import status


# Import request data models for user login and signup
from ecom_api.models.data_table_models.public_user.user_signup_request import (
    UserSignupRequestDataModel,
)
from ecom_api.models.data_table_models.public_user.user_login_request import (
    UserLoginRequestDataModel,
)
from ecom_api.models.data_table_models.public_user.create_order_request import CreateOrderRequestDataModel

# Import services for user login, signup, and session handling
from ecom_api.services.public_user.user_signup import UserSignupService
from ecom_api.services.public_user.user_login import UserLoginService
from ecom_api.services.public_user.user_session import UserSessionService
from ecom_api.services.public_user.order import OrderService

# Import response data models for user login, signup, and session handling
from ecom_api.models.response_models.public_user.user_signup import UserSignupResponseModel
from ecom_api.models.response_models.public_user.user_login import UserLoginResponseModel
from ecom_api.models.response_models.public_user.create_user_session import (
    CreateUserSessionResponseModel,
)
from ecom_api.models.response_models.public_user.check_user_session import (
    CheckUserSessionResponseModel,
)
from ecom_api.models.response_models.public_user.order_request import OrderRequestResponseModel

from ecom_api.logger import Logger

# Instantiate the signup and login services
signup_service = UserSignupService()
login_service = UserLoginService()
logger = Logger()

def public_users_routes(app):
    # Route for user login
    @app.route("/user-login", methods=["POST"])
    def login():
        try:
            request_data = request.get_json()
            
            if not request_data:
                logger.warning("Request body is empty or not in JSON format")
                return jsonify(error="Request body is empty or not in JSON format."), status.HTTP_400_BAD_REQUEST
            
            # Parse and validate user login data
            user_data = UserLoginRequestDataModel(request_data)

            # If the user data is invalid, return an error message
            if not user_data.isValid():
                logger.warning(f"User data is invalid. {user_data.error_message}")
                
                return jsonify(error=user_data.error_message), 400

            # Call the login service with the validated user data
            login_response = login_service.user_login(user_data)

            # Create a response data model object with the login response data
            response_data = UserLoginResponseModel(login_response)

            # Return the response data as JSON
            return jsonify(response_data.to_dict())

        except Exception as err:
            logger.error(f"An unexpected error occurred in user-login route | Error: {err} | Traceback: {traceback.format_exc()}")
            return jsonify({"error": "An unexpected error occurred. Please contact the support team."}), 500

    # Route for user signup
    @app.route("/user-signup", methods=["POST"])
    def sign_up():
        try:
            
            request_data = request.get_json()
            
            if not request_data:
                logger.warning("Request body is empty or not in JSON format")
                return jsonify(error="Request body is empty or not in JSON format."), status.HTTP_400_BAD_REQUEST
            
            # Parse and validate user signup data
            user_data = UserSignupRequestDataModel(request_data)

            # If the user data is invalid, return an error message
            if not user_data.isValid():
                return jsonify(error=user_data.error_message), 400

            # Call the signup service with the validated user data
            signup_response = signup_service.user_signup(user_data)

            # Create a response data model object with the signup response data
            response_data = UserSignupResponseModel(signup_response)

            # Return the response data as JSON
            return jsonify(response_data.to_dict())

        except Exception as err:
            logger.error(f"An unexpected error occurred in user-signup route | Error: {err} | Traceback: {traceback.format_exc()}")
            return jsonify({"error": "An unexpected error occurred. Please contact the support team."}), 500

    # Route for creating a user session
    @app.route("/user/create-session/<user_id>", methods=["POST"])
    def create_session_user(user_id):
        try:
            # Instantiate the user session service
            user_session_service = UserSessionService()

            # Call the session service to create a new session for the provided user ID
            response = user_session_service.create_session(user_id)

            if not response:
                logger.warning("Failed to create session")
                return jsonify({"error": "Failed to create session"}), 500
            
            # Create a response data model object with the new session GUID
            response_data = CreateUserSessionResponseModel(response.guid)

            # Return the response data as JSON
            return jsonify(response_data.to_dict())

        except Exception as err:
            logger.error(f"An unexpected error occurred in create-session route | Error: {err} | Traceback: {traceback.format_exc()}")
            return jsonify({"error": "Failed to create session"}), 500

    # Route for checking the validity of a user cookie
    @app.route("/user/check-cookie-validity/<guid>", methods=["POST"])
    def check_cookie_validity_user(guid):
        try:
            # Instantiate the user session service
            user_session_service = UserSessionService()

            # Call the session service to check the validity of the provided GUID
            response = user_session_service.check_session_user(guid)

            # Create a response data model object with the session validity and username
            response_data = CheckUserSessionResponseModel(
                response.session_valid, response.username, response.user_id
            )

            # Return the response data as JSON
            return jsonify(response_data.to_dict())

        except Exception as err:
            logger.error(f"An unexpected error occurred in check-cookie-validity route | Error: {err} | Traceback: {traceback.format_exc()}")
            return jsonify({"error": "Failed to check cookie"}), 500
            
    @app.route("/create-order", methods=["POST"])
    def process_orders():
        try:
            request_data = request.get_json()
            
            if not request_data:
                return jsonify(error="Request body is empty or not in JSON format."), status.HTTP_400_BAD_REQUEST
            
            
            order_request_data = CreateOrderRequestDataModel(request_data)
            
            order_service = OrderService()

            response = order_service.create_order(order_request_data)
            
            if response[0]:
                response_data = OrderRequestResponseModel(response[0], response[3], "Order placed successfully", None , response[2])
                return jsonify(response_data.to_dict())

            response_data = OrderRequestResponseModel(response[0], response[3],f"Insufficient stock for {response[2]}")

            return jsonify(response_data.to_dict())

        except Exception as err:
            logger.error(f"An unexpected error occurred in create-order route | Error: {err} | Traceback: {traceback.format_exc()}")
            return jsonify({"error": "Failed to create an order"}), 500
            
    
    @app.route("/process-paid-orders", methods=["GET"])
    def delete_reservations():
        try:
            user_id = request.args.get("user_id")
            order_id = request.args.get("order_id")
            
            order_service = OrderService()

            response = order_service.process_paid_orders(user_id, order_id)
            
            if response[0]:
                return jsonify(success = True)
            
            return jsonify(success = False, message = response[1])
            

        except Exception as err:
            logger.error(f"An unexpected error occurred in process-paid-orders route | Error: {err} | Traceback: {traceback.format_exc()}")
            return jsonify({"error": "Failed to process the order"}), 500
    