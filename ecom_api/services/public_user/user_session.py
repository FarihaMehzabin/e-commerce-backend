import uuid, traceback
from services.hashing import Hashing
from models.data_table_models.public_user.create_user_session_result import CreateUserSessionResultDataModel
from models.data_table_models.public_user.check_user_session_result import CheckUserSessionResultDataModel


class UserSessionService:
    def __init__(self):
        self.hash = Hashing()
        
    def create_session(self, user_id):
        guid_id = str(uuid.uuid4())
        
        hashed_guid = hash.hash_guid(guid_id)
        
        try:

            self.db.insert(
                f"INSERT INTO session (guid, user_id) VALUES (%s, %s)", (guid, user_id)
            )
            
            response = CreateUserSessionResultDataModel(hashed_guid)
            
            return response

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

            return False
        
        
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
                
                response = CheckUserSessionResultDataModel(True, data[0] + data[1])
                
                return response

        return CheckUserSessionResultDataModel(False, 'No user found')
                