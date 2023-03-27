import traceback
from services.db_functions import DbFunctions
from db.user_db import UserDB
from models.data_table_models.public_user.user_signup_result import UserSignupResultDataModel

class UserSignupService:
    def __init__(self):
        self.user_db = UserDB()
        
    def user_signup(self, user):
        rowcount, id = self.user_db.create_user(user)

        if rowcount:
            response = UserSignupResultDataModel(rowcount, f"New user signed up! Welcome :)", False, id)
            print(response.error)
            
        else:
            response = UserSignupResultDataModel(False, "Username taken. Please try again.", True)

        return response
        
        
        