import traceback
from ecom_api.services.db_functions import DbFunctions 
from ecom_api.logger import Logger

class CompanySessionDB:
    def __init__(self):
        self.db = DbFunctions()
        self.logger = Logger()

    def create_session(self, hashed_guid, comp_id):
        try:
            self.db.insert(
                f"INSERT INTO session (guid, company_id) VALUES (%s, %s)",
                (hashed_guid, comp_id),
            )
            self.logger.info("Successfully created session.")
            return True
        except Exception as e:
            self.logger.error(f"Error creating session. Error: {e}")
            raise

    def get_session_by_guid(self, guid):
        try:
            res = self.db.fetch(
                f"SELECT guid, company_id FROM session WHERE guid = '{guid}'"
            )
            self.logger.info(f"Retrieved session with guid: {guid}")
            return res[0] if res else None
        except Exception as e:
            self.logger.error(f"Error retrieving session with guid: {guid}. Error: {e}")
            raise

    def get_user_by_id(self, comp_id):
        try:
            res = self.db.fetch(f"SELECT name FROM company WHERE id = '{comp_id}'")
            self.logger.info(f"Retrieved user with id: {comp_id}")
            return res[0] if res else None
        except Exception as e:
            self.logger.error(f"Error retrieving user with id: {comp_id}. Error: {e}")
            raise
