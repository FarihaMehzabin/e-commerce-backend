import traceback
from ecom_api.services.db_functions import DbFunctions
from ecom_api.db.user_db import UserDB
from ecom_api.models.data_table_models.public_user.user_signup_result import UserSignupResultDataModel
from ecom_api.logger import Logger

logger = Logger()

class UserSignupService:
    def __init__(self):
        self.user_db = UserDB()
        
    def user_signup(self, user):
        rowcount, id = self.user_db.create_user(user)

        if rowcount:
            logger.info(f"New user created successfully. User id {id}")
            response = UserSignupResultDataModel(rowcount, f"New user signed up! Welcome :)", False, id)
            
        else:
            response = UserSignupResultDataModel(False, "Username taken. Please try again.", True)
            
            logger.warning("user signup unsuccessful")

        return response
        
        
        