from hashing import Hashing
from db_functions import DbFunctions
import traceback

class Login:
    def __init__(self):
        self.hash = Hashing()
        self.db = DbFunctions()
        
    def user_login(self, uname, password):

        res = self.db.fetch(f"SELECT * FROM user WHERE username = '{uname}'")

        data = res[0]

        if data is not None:

            hash = data[4]

            return self.hash.compare_pass(password, hash), data[0]

        return False
    
    def comp_login(self, uname, password):

        res = self.db.fetch(f"SELECT * FROM company WHERE username = '{uname}'")

        data = res[0]
        
        if data is not None:

            hash = data[3]

            return self.hash.compare_pass(password, hash), data[0]

        return False