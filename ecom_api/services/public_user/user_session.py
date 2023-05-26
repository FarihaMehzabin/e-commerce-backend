import uuid
from ecom_api.services.hashing import Hashing
from ecom_api.models.data_table_models.public_user.create_user_session_result import CreateUserSessionResultDataModel
from ecom_api.models.data_table_models.public_user.check_user_session_result import CheckUserSessionResultDataModel
from ecom_api.db.user_session_db import UserSessionDB
from ecom_api.logger import Logger

logger = Logger()

class UserSessionService:
    def __init__(self):
        self.hash = Hashing()
        self.user_session_db = UserSessionDB()

    def create_session(self, user_id):
        guid_id = str(uuid.uuid4())
        hashed_guid = self.hash.hash_guid(guid_id)

        if self.user_session_db.create_session(hashed_guid, user_id):
            logger.info(f"session created. UserID: {user_id}")
            
            response = CreateUserSessionResultDataModel(hashed_guid)
            
            return response
        else:
            
            logger.warning(f"Failed to create session. UserID: {user_id}")
            
            return False

    def check_session_user(self, guid):
        data = self.user_session_db.get_session_by_guid(guid)

        if data:
            user_id = data[1]
            
            first_name = data[2]
            
            last_name = data[3]
            
            logger.info(f"session found for UserID: {user_id}")

            response = CheckUserSessionResultDataModel(True, first_name+last_name, user_id)
            return response


        logger.warning(f"Failed to find session for GUID: {guid}")
        
        return CheckUserSessionResultDataModel(False, 'No user found', 0)