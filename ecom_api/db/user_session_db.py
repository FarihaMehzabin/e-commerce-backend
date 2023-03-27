import traceback
from services.db_functions import DbFunctions 

class UserSessionDB:
    def __init__(self):
        self.db = DbFunctions()

    def create_session(self, hashed_guid, user_id):
        try:
            self.db.insert(
                f"INSERT INTO session (guid, user_id) VALUES (%s, %s)", (hashed_guid, user_id)
            )
            return True
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
            return False

    def get_session_by_guid(self, guid):
        res = self.db.fetch(
            f"SELECT guid, user_id FROM session WHERE guid = '{guid}'"
        )
        return res[0] if res else None

    def get_user_by_id(self, user_id):
        res = self.db.fetch(
            f"SELECT first_name, last_name FROM user WHERE id = '{user_id}'"
        )
        return res[0] if res else None
