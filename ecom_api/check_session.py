from hashing import Hashing
from db_functions import DbFunctions


class CheckSession:
    
    def __init__(self):
        self.hash = Hashing()
        self.db = DbFunctions()
    
    def check_session_comp(self, guid):

        res = self.db.fetch(
            f"SELECT guid, company_id FROM session WHERE guid = '{guid}'"
        )
        
        data = res[0]

        guid = data[0]

        comp_id = data[1]
        
        print(f"company id: {comp_id}")

        if comp_id is not None:

            res = self.db.fetch(f"SELECT name FROM company WHERE id = '{comp_id}'")
            
            data = res[0]
            
            if guid is not None:
                return True, data[0]


        return False, "no company"
    
    
    def check_session_user(self, guid):

        res = self.db.fetch(
            f"SELECT guid, user_id FROM session WHERE guid = '{guid}'"
        )
        
        data = res[0]

        guid = data[0]

        user_id = data[1]
        
        print(f"user id: {user_id}")

        if user_id is not None:

            res = self.db.fetch(
                f"SELECT first_name, last_name FROM user WHERE id = '{user_id}'"
            )
            
            data = res[0]

            if guid is not None:
                return True, data[0] + data[1]

        return False, 'No user found'