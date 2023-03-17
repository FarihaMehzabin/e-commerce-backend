from hashing import Hashing
from db_functions import DbFunctions
import traceback


class SignUp:
    
    def __init__(self):
        self.hash = Hashing()
        self.db = DbFunctions()
    
    def user_signup(self, fname, lname, uname, password):

        try:
            hashed_pass = self.hash.hash_pass(password)

            rowcount, id = self.db.insert(
                f"INSERT INTO user (username, first_name, last_name, password) VALUES (%s, %s, %s, %s)",
                (uname, fname, lname, hashed_pass),
            )

            return rowcount, id

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

            return False, 1
        
    def comp_signup(self, cname, uname, password):

        try:

            hashed_pass = self.hash.hash_pass(password)

            rowcount, id = self.db.insert(
                f"INSERT INTO company (name, username, password) VALUES (%s, %s, %s)",
                (cname, uname, hashed_pass),
            )

            return rowcount, id

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

            return False, 1    