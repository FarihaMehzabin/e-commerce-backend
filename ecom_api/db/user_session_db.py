import traceback
from ecom_api.services.db_functions import DbFunctions 
from ecom_api.logger import Logger

class UserSessionDB:
    def __init__(self):
        self.db = DbFunctions()
        self.logger = Logger()

    def create_session(self, hashed_guid, user_id):
        try:
            self.db.insert(
                f"INSERT INTO session (guid, user_id) VALUES (%s, %s)", (hashed_guid, user_id)
            )
            self.logger.info("Session created successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Error creating session. Error: {e}")
            raise

    def get_session_by_guid(self, guid):
        try:
            res = self.db.fetch(
            f"""
            SELECT 
                session.guid, 
                session.user_id, 
                user.first_name, 
                user.last_name 
            FROM 
                session 
            INNER JOIN 
                user 
            ON 
                session.user_id = user.id
            WHERE 
                session.guid = '{guid}'
            """
            )
            self.logger.info(f"Retrieved session with guid: {guid}")
            return res[0] if res else None
        except Exception as e:
            self.logger.error(f"Error retrieving session with guid: {guid}. Error: {e}")
            raise