import traceback
from services.hashing import Hashing
from services.db_functions import DbFunctions
from models.data_table_models.public_user.user_login_result import UserLoginResultDataModel


class UserLoginService:
    def __init__(self):
        self.hash = Hashing()
        self.db = DbFunctions()
    
    def user_login(self, user):

        res = self.db.fetch(f"SELECT * FROM user WHERE username = '{user.username}'")

        data = res[0]

        if data is not None:

            hash = data[4]
            
            response = UserLoginResultDataModel(self.hash.compare_pass(user.password, hash),f"Logged in! Welcome :) {user.username}", False, data[0])

            return response

        return UserLoginResultDataModel(False,"Invalid Credentials. Please try again.", True,)
