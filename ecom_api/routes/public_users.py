import traceback
from flask import request


from models.data_table_models.public_user.user_signup_request import (
    UserSignupRequestDataModel,
)
from models.data_table_models.public_user.user_login_request import UserLoginRequestDataModel

from services.public_user.user_signup import UserSignupService
from services.public_user.user_login import UserLoginService
from services.public_user.user_session import UserSessionService

from models.response_models.public_user.user_signup import UserSignupResponseModel
from models.response_models.public_user.user_login import UserLoginResponseModel
from models.response_models.public_user.create_user_session import (
    CreateUserSessionResponseModel
)
from models.response_models.public_user.check_user_session import (
   CheckUserSessionResponseModel,
)

signup_service = UserSignupService()
login_service = UserLoginService()

def public_users_routes(app):
    
    #  Public users login
    @app.route("/user-login/", methods=['POST'])
    def login():
        
        data = request.get_json()

        user_data = UserLoginRequestDataModel(data)

        login_response = login_service.comp_login(user_data)

        if login_response.user_logged:
            return UserLoginResponseModel(
                f"Logged in! Welcome :)", False, login_response.user_id
            )

        return UserLoginResponseModel(
            "Invalid Credentials. Please try again.", True, 0
        )
        

        
            # user, user_id  = db.user_login(username,password)
            # if user:
            #     return jsonify(message = f"Logged in! Welcome, {username} :)", error= False, u_id = user_id)
            # else:
            #     return jsonify(message = 'Invalid Credentials. Please try again.', error = True)
                

    # Public user signup
    @app.route("/user-signup/", methods=['GET'])
    def sign_up(fname, lname, username, password):
        
        data = request.get_json()

        # creating a signup data model with the data received from the frontend
        company_data = UserSignupRequestDataModel(data)

        # pass the object to the service
        # using the company signup service model to do db operations and hashing
        # returns a signup response data model
        signup_response = signup_service.comp_signup(company_data)

        # using the response to send reponse model back to the client
        if signup_response.user_created:

            return UserSignupResponseModel(
                f"New user signed up! Welcome :)",
                False,
                signup_response.user_id,
            )

        return UserSignupResponseModel("Username taken. Please try again.", True, 0)
            
            # user, user_id = db.user_signup(fname, lname, username, password)
            
            # if user:
            #     return jsonify(message = f"New user signed up! Welcome, {username} :)", error= False, u_id = user_id)
            # else:
            #     return jsonify(message = 'Username taken. Please try again.', error = True)
            
            
        
    # creates a session for the public users
    # generates a GUID, hash it and adds it along with the user id to the 
    # session table
    @app.route("/user/create-session/<user_id>", methods = ["GET"])
    def create_session_user(user_id):
        
        
        response = UserSessionService.create_session(user_id)

        return CreateUserSessionResponseModel(response.guid)
        
        # guid_id = str(uuid.uuid4())
        
        # hashed_guid = hash.hash_guid(guid_id)
        
        # db.add_to_session_user(hashed_guid, user_id)
        
        # return jsonify( guid = hashed_guid )

            
    # check is the cookie sent by the client for login is valid. This endpoint is 
    # for the public users only. It returns a booolean to indicate whether 
    # the cookie is valid and the name of the user
    @app.route("/user/check-cookie-validity/<guid>", methods=['GET',"POST"])
    def check_cookie_validity_user(guid):
        
        try:
            response = UserSessionService.check_session_user(guid)

            return CheckUserSessionResponseModel(
                response.session_valid, response.username
            )
        
        # try:
        #     is_session_valid, u = db.check_session_user(guid)
            
        #     return jsonify(check = is_session_valid, user = u)
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")