import traceback
from ecom_api.models.data_table_models.create_company_signup import CreateCompanySignupData
from hashing import Hashing
from flask import jsonify
from db import Db
import uuid
from models.data_table_models.create_company_signup import CreateCompanySignupDataModel
from services.company_signup import CompanySignupService
from models.response_models.company_signup import CompanySignupResponseModel

db = Db()
hash = Hashing()
signup_service = CompanySignupService()

def company_users_routes(app):    
    # company users signup
    @app.route("/company/user/signup/<cname>/<username>/<password>", methods=['GET'])
    def comp_sign_up(cname, username, password):
            
            # creating a signup data model with the data received from the frontend
            company_data = CreateCompanySignupDataModel(cname, username, password)
            
            # pass the object to the service
            # using the company signup service model to do db operations and hashing
            # returns a signup response data model
            signup_response = signup_service.comp_signup(company_data)
            
            # using the response to send reponse model back to the client
            if signup_response.user_created:
                
                return CompanySignupResponseModel(f"New user signed up! Welcome, {username} :)", False, signup_response.company_id )
                # return jsonify(message = f"New user signed up! Welcome, {username} :)", error= False, comp_id = signup_response.company_id)
            else:
                
                return CompanySignupResponseModel('Username taken. Please try again.', True, 0 )

                # return jsonify(message = 'Username taken. Please try again.', error = True, comp_id = 0)


    # company users login
    @app.route("/company/user/login/<username>/<password>", methods=['GET'])
    def comp_login(username, password):
        
            user, company_id = db.comp_login(username,password)
            
            print(user)
            
            if user:
                return jsonify(message = f"Logged in! Welcome, {username} :)", error= False, comp_id = company_id)
            else:
                return jsonify(message = 'Invalid Credentials. Please try again.', error = True)
            
    
    # creates a session for the company users
    # generates a GUID, hash it and adds it along with the company id to the 
    # session table
    @app.route("/company/create-session/<comp_id>", methods = ["GET"])
    def create_session_comp(comp_id):
        
        guid_id = str(uuid.uuid4())
        
        hashed_guid = hash.hash_guid(guid_id)
        
        db.add_to_session_comp(hashed_guid, comp_id)
        
        return jsonify( guid = hashed_guid )
    
    # check is the cookie sent by the client for login is valid. This endpoint is 
    # for the company users only. It returns a booolean to indicate whether 
    # the cookie is valid and the name of the company
    @app.route("/company/check-cookie-validity/<guid>", methods=['GET',"POST"])
    def check_cookie_validity_comp(guid):
        try:
            is_session_valid, company = db.check_session_comp(guid)
            
            return jsonify(check = is_session_valid, comp = company)
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
            
    