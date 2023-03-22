import traceback
from services.hashing import Hashing
from services.db_functions import DbFunctions
from models.data_table_models.public_user.user_signup_result import UserSignupResultDataModel

class UserSignupService:
    def __init__(self):
        self.hash = Hashing()
        self.db = DbFunctions()
        
    def user_signup(self, user):

        try:
            hashed_pass = self.hash.hash_pass(user.password)

            rowcount, id = self.db.insert(
                f"INSERT INTO user (username, first_name, last_name, password) VALUES (%s, %s, %s, %s)",
                (user.username, user.first_name, user.last_name, hashed_pass),
            )

            response = UserSignupResultDataModel(rowcount, id)

            return response
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

            return UserSignupResultDataModel(False, 1)