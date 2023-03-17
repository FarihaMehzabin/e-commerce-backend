import traceback
from hashing import Hashing
from db_functions import DbFunctions

class AddSession:
    
    def __init__(self):
        self.hash = Hashing()
        self.db = DbFunctions()
    
    def add_to_session_comp(self, guid, comp_id):
        try:

            self.db.insert(
                f"INSERT INTO session (guid, company_id) VALUES (%s, %s)",
                (guid, comp_id),
            )

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

            return False

    def add_to_session_user(self, guid, user_id):
        try:

            self.db.insert(
                f"INSERT INTO session (guid, user_id) VALUES (%s, %s)", (guid, user_id)
            )

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

            return False