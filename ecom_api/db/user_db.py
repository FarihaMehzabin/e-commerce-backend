from ecom_api.services.db_functions import DbFunctions 
from ecom_api.services.hashing import Hashing
import traceback

class UserDB:
    def __init__(self):
        self.db = DbFunctions()
        self.hash = Hashing()

    # Get user by username
    def get_user_by_username(self, username):
        res = self.db.fetch(f"SELECT * FROM user WHERE username = '{username}'")
        return res[0] if res else None

    # Create a new user with the provided user information
    def create_user(self, user):
        try:
            hashed_pass = self.hash.hash_pass(user.password)

            rowcount, id = self.db.insert(
                f"INSERT INTO user (username, first_name, last_name, password) VALUES (%s, %s, %s, %s)",
                (user.username, user.first_name, user.last_name, hashed_pass),
            )
            return rowcount, id
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
            return None, None
    
