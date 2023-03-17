import traceback
from hashing import Hashing
from flask import jsonify
from db import Db
import uuid


db = Db()
hash = Hashing()



def public_users_routes(app):
    
    #  Public users login
    @app.route("/user-login/<username>/<password>", methods=['GET'])
    def login(username, password):
        
            user, user_id  = db.user_login(username,password)
            if user:
                return jsonify(message = f"Logged in! Welcome, {username} :)", error= False, u_id = user_id)
            else:
                return jsonify(message = 'Invalid Credentials. Please try again.', error = True)
                

    # Public user signup
    @app.route("/user-signup/<fname>/<lname>/<username>/<password>", methods=['GET'])
    def sign_up(fname, lname, username, password):
            
            user, user_id = db.user_signup(fname, lname, username, password)
            
            if user:
                return jsonify(message = f"New user signed up! Welcome, {username} :)", error= False, u_id = user_id)
            else:
                return jsonify(message = 'Username taken. Please try again.', error = True)
            
            
        
    # creates a session for the public users
    # generates a GUID, hash it and adds it along with the user id to the 
    # session table
    @app.route("/user/create-session/<user_id>", methods = ["GET"])
    def create_session_user(user_id):
        
        guid_id = str(uuid.uuid4())
        
        hashed_guid = hash.hash_guid(guid_id)
        
        db.add_to_session_user(hashed_guid, user_id)
        
        return jsonify( guid = hashed_guid )

            
    # check is the cookie sent by the client for login is valid. This endpoint is 
    # for the public users only. It returns a booolean to indicate whether 
    # the cookie is valid and the name of the user
    @app.route("/user/check-cookie-validity/<guid>", methods=['GET',"POST"])
    def check_cookie_validity_user(guid):
        try:
            is_session_valid, u = db.check_session_user(guid)
            
            return jsonify(check = is_session_valid, user = u)
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")