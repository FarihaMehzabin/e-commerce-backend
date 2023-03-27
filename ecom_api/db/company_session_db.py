import traceback
from services.db_functions import DbFunctions 

class CompanySessionDB:
    def __init__(self):
        self.db = DbFunctions()

    def create_session(self, hashed_guid, comp_id):
        try:
            self.db.insert(
                f"INSERT INTO session (guid, company_id) VALUES (%s, %s)",
                (hashed_guid, comp_id),
            )
            return True
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
            return False

    def get_session_by_guid(self, guid):
        res = self.db.fetch(
            f"SELECT guid, company_id FROM session WHERE guid = '{guid}'"
        )
        return res[0] if res else None

    def get_user_by_id(self, comp_id):
        res = self.db.fetch(f"SELECT name FROM company WHERE id = '{comp_id}'")
        return res[0] if res else None
