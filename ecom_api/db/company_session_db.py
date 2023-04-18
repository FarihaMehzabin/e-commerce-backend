import traceback
from ecom_api.services.db_functions import DbFunctions 


class CompanySessionDB:
    def __init__(self):
        self.db = DbFunctions()

    # Create a new session with the provided hashed GUID and company ID
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

    # Get session details by GUID
    def get_session_by_guid(self, guid):
        res = self.db.fetch(
            f"SELECT guid, company_id FROM session WHERE guid = '{guid}'"
        )
        return res[0] if res else None

    # Get user details by company ID
    def get_user_by_id(self, comp_id):
        res = self.db.fetch(f"SELECT name FROM company WHERE id = '{comp_id}'")
        return res[0] if res else None
