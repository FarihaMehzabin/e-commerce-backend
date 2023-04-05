import traceback
from flask import request, jsonify
from flask_api import status


from models.data_table_models.public_user.user_signup_request import (
    UserSignupRequestDataModel,
)
from models.data_table_models.public_user.user_login_request import (
    UserLoginRequestDataModel,
)

from services.public_user.user_signup import UserSignupService
from services.public_user.user_login import UserLoginService
from services.public_user.user_session import UserSessionService

from models.response_models.public_user.user_signup import UserSignupResponseModel
from models.response_models.public_user.user_login import UserLoginResponseModel
from models.response_models.public_user.create_user_session import (
    CreateUserSessionResponseModel,
)
from models.response_models.public_user.check_user_session import (
    CheckUserSessionResponseModel,
)

signup_service = UserSignupService()
login_service = UserLoginService()


def public_users_routes(app):

    @app.route("/user-login", methods=["POST"])
    def login():
        try:    
            user_data = UserLoginRequestDataModel(request.get_json())
            
            # validation
            if user_data.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
                return jsonify(error = user_data.error_message
)
            login_response = login_service.user_login(user_data)
            
            response_data = UserLoginResponseModel(login_response)

            return jsonify(response_data.to_dict())
        
        except Exception as err:
                print(traceback.format_exc())
                print(f"{err}")

    
    @app.route("/user-signup", methods=["POST"])
    def sign_up():
        try:
            user_data = UserSignupRequestDataModel(request.get_json())

            # validation
            if user_data.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
                return jsonify(error = user_data.error_message)

            signup_response = signup_service.user_signup(user_data)

            response_data = UserSignupResponseModel(signup_response)

            return jsonify(response_data.to_dict())

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")


    @app.route("/user/create-session/<user_id>", methods=["POST"])
    def create_session_user(user_id):
        try:
            
            user_session_service = UserSessionService()
            
            response = user_session_service.create_session(user_id)
            
            response_data = CreateUserSessionResponseModel(response.guid)

            return jsonify(response_data.to_dict())

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")


    @app.route("/user/check-cookie-validity/<guid>", methods=["POST"])
    def check_cookie_validity_user(guid):
        try:
            
            user_session_service = UserSessionService()
            
            response = user_session_service.check_session_user(guid)
            
            response_data = CheckUserSessionResponseModel(
                response.session_valid, response.username
            )

            return jsonify(response_data.to_dict())

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
