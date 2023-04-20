import traceback
from flask import request, jsonify
from flask_api import status
import logging

# Configure the logging
logging.basicConfig(level=logging.ERROR)

# Import request data models for handling company login and signup requests
from ecom_api.models.data_table_models.company.company_login_request import (
    CompanyLoginRequestDataModel,
)
from ecom_api.models.data_table_models.company.company_signup_request import (
    CompanySignupRequestDataModel,
)

# Import response data models for handling company-related responses
from ecom_api.models.response_models.company.check_company_session import (
    CheckCompanySessionResponseModel,
)
from ecom_api.models.response_models.company.company_login import CompanyLoginResponseModel
from ecom_api.models.response_models.company.company_signup import CompanySignupResponseModel
from ecom_api.models.response_models.company.create_company_session import (
    CreateCompanySessionResponseModel,
)

# Import services for managing company login, session, and signup
from ecom_api.services.company.company_login import CompanyLoginService
from ecom_api.services.company.company_session import CompanySessionService
from ecom_api.services.company.company_signup import CompanySignupService

# Instantiate the company signup and login services
signup_service = CompanySignupService()
login_service = CompanyLoginService()

# Define company users routes
def company_users_routes(app):
    
    @app.route("/company/user/signup", methods=["POST"])
    def comp_sign_up():
        try:
            
            request_data = request.get_json()
            
            if not request_data:
                return jsonify(error="Request body is empty or not in JSON format."), status.HTTP_400_BAD_REQUEST
            
            # Parse the request data and create a data model object
            company_data = CompanySignupRequestDataModel(request_data)

            # If there was an error in parsing the request data, return the error message
            if not company_data.isValid():
                return jsonify(error=company_data.error_message), 400

            # Process the signup request using the signup service
            signup_response = signup_service.comp_signup(company_data)

            # Create a response data model object with the signup response
            response_data = CompanySignupResponseModel(signup_response)

            # Return the response data as JSON
            return jsonify(response_data.to_dict())

        except Exception as err:
            print(traceback.format_exc())
            logging.error(f"An unexpected error occurred: {err}")
            return jsonify(error="An unexpected error occurred. Please contact the support team."), status.HTTP_500_INTERNAL_SERVER_ERROR


    # Route for company user login
    @app.route("/company/user/login", methods=["POST"])
    def comp_login():
        try:
            # Parse the request data and create a data model object
            company_data = CompanyLoginRequestDataModel(request.get_json())

            # If there was an error in parsing the request data, return the error message
            if not company_data.isValid():
                return jsonify(error=company_data.error_message), 400

            # Process the login request using the login service
            login_response = login_service.comp_login(company_data)

            # Create a response data model object with the login response
            response_data = CompanyLoginResponseModel(login_response)

            # Return the response data as JSON
            return jsonify(response_data.to_dict())

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

    # Route for creating a company session
    @app.route("/company/create-session/<comp_id>", methods=["POST"])
    def create_session_comp(comp_id):
        try:
            # Instantiate the company session service
            company_service = CompanySessionService()
            
            # Create a new session using the provided company ID
            response = company_service.create_session(comp_id)
            
            if not response:
                return jsonify({"error": "Failed to create session"}), 500

            # Create a response data model object with the generated session GUID
            response_data = CreateCompanySessionResponseModel(response.guid)

            # Return the response data as JSON
            return jsonify(response_data.to_dict())

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

    # Route for checking the validity of a company cookie
    @app.route("/company/check-cookie-validity/<guid>", methods=["POST"])
    def check_cookie_validity_comp(guid):
        try:
            # Instantiate the company session service
            company_service = CompanySessionService()

            # Check the session validity for the provided GUID
            response = company_service.check_session_comp(guid)

            # Create a response data model object with the session validity and company name
            response_data = CheckCompanySessionResponseModel(
                response.session_valid, response.company_name
            )

            # Return the response data as JSON
            return jsonify(response_data.to_dict())

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")


