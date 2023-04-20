import traceback
from flask import request, jsonify
from flask_api import status
import logging

# Configure the logging
logging.basicConfig(level=logging.ERROR)

# Import request data models for user login and signup
from ecom_api.models.data_table_models.public_user.user_signup_request import (
    UserSignupRequestDataModel,
)
from ecom_api.models.data_table_models.public_user.user_login_request import (
    UserLoginRequestDataModel,
)

# Import services for user login, signup, and session handling
from ecom_api.services.public_user.user_signup import UserSignupService
from ecom_api.services.public_user.user_login import UserLoginService
from ecom_api.services.public_user.user_session import UserSessionService

# Import response data models for user login, signup, and session handling
from ecom_api.models.response_models.public_user.user_signup import UserSignupResponseModel
from ecom_api.models.response_models.public_user.user_login import UserLoginResponseModel
from ecom_api.models.response_models.public_user.create_user_session import (
    CreateUserSessionResponseModel,
)
from ecom_api.models.response_models.public_user.check_user_session import (
    CheckUserSessionResponseModel,
)

# Instantiate the signup and login services
signup_service = UserSignupService()
login_service = UserLoginService()


def public_users_routes(app):
    # Route for user login
    @app.route("/user-login", methods=["POST"])
    def login():
        try:
            request_data = request.get_json()
            
            if not request_data:
                return jsonify(error="Request body is empty or not in JSON format."), status.HTTP_400_BAD_REQUEST
            
            # Parse and validate user login data
            user_data = UserLoginRequestDataModel(request_data)

            # If the user data is invalid, return an error message
            if not user_data.isValid():
                return jsonify(error=user_data.error_message), 400

            # Call the login service with the validated user data
            login_response = login_service.user_login(user_data)

            # Create a response data model object with the login response data
            response_data = UserLoginResponseModel(login_response)

            # Return the response data as JSON
            return jsonify(response_data.to_dict())

        except Exception as err:
            print(traceback.format_exc())
            logging.error(f"An unexpected error occurred: {err}")
            return jsonify(error="An unexpected error occurred. Please contact the support team."), status.HTTP_500_INTERNAL_SERVER_ERROR

    # Route for user signup
    @app.route("/user-signup", methods=["POST"])
    def sign_up():
        try:
            
            request_data = request.get_json()
            
            if not request_data:
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
            print(traceback.format_exc())
            print(f"{err}")

    # Route for creating a user session
    @app.route("/user/create-session/<user_id>", methods=["POST"])
    def create_session_user(user_id):
        try:
            # Instantiate the user session service
            user_session_service = UserSessionService()
            
            if not response:
                return jsonify({"error": "Failed to create session"}), 500

            # Call the session service to create a new session for the provided user ID
            response = user_session_service.create_session(user_id)

            # Create a response data model object with the new session GUID
            response_data = CreateUserSessionResponseModel(response.guid)

            # Return the response data as JSON
            return jsonify(response_data.to_dict())

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

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
                response.session_valid, response.username
            )

            # Return the response data as JSON
            return jsonify(response_data.to_dict())

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

