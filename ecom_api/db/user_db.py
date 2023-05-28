from ecom_api.services.db_functions import DbFunctions 
from ecom_api.services.hashing import Hashing
from ecom_api.logger import Logger

class UserDB:
    def __init__(self):
        self.db = DbFunctions()
        self.hash = Hashing()
        self.logger = Logger()

    def get_user_by_username(self, username):
        try:
            res = self.db.fetch(f"SELECT * FROM user WHERE username = '{username}'")
            self.logger.info(f"Retrieved user with username: {username}")
            return res[0] if res else None
        except Exception as e:
            self.logger.error(f"Error retrieving user with username: {username}. Error: {e}")
            raise
    
    def get_user_by_id(self, user_id):
        try:
            
            self.logger.debug(f"SELECT * FROM user WHERE id = '{user_id}'")
            res = self.db.fetch(f"SELECT * FROM user WHERE id = '{user_id}'")
            self.logger.info(f"Retrieved user with user_id: {res}")
            return res[0] if res else None
        
        except Exception as e:
            self.logger.error(f"Error retrieving user with user_id: {user_id}. Error: {e}")
            raise
    
    def create_user(self, user):
        try:
            hashed_pass = self.hash.hash_pass(user.password)

            rowcount, id = self.db.insert(
                f"INSERT INTO user (username, first_name, last_name, password, email) VALUES (%s, %s, %s, %s, %s)",
                (user.username, user.first_name, user.last_name, hashed_pass, user.email),
            )
            self.logger.info("User created successfully.")
            return rowcount, id
        except Exception as e:
            self.logger.error(f"Error creating user. Error: {e}")
            raise