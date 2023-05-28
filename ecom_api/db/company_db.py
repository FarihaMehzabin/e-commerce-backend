from ecom_api.services.db_functions import DbFunctions 
from ecom_api.services.hashing import Hashing
from ecom_api.logger import Logger
import traceback

class CompanyDB:
    def __init__(self):
        self.db = DbFunctions()
        self.hash = Hashing()
        self.logger = Logger()

    def get_company_by_username(self, username):
        try:
            res = self.db.fetch(f"SELECT * FROM company WHERE username = '{username}'")
            self.logger.info(f"Retrieved company with username: {username}")
            return res[0] if res else None
        except Exception as e:
            self.logger.error(f"Error retrieving company with username: {username}. Error: {e}")
            raise

    def create_company_user(self, company):
        try:
            hashed_pass = self.hash.hash_pass(company.password)
            rowcount, id = self.db.insert(
                f"INSERT INTO company (name, username, password, email) VALUES (%s, %s, %s, %s)",
                (company.company, company.username, hashed_pass, company.email),
            )
            self.logger.info(f"Successfully created company user. Company id is {id}")
            return rowcount, id
        except Exception as e:
            self.logger.error(f"Error creating company user. Error: {e}")
            raise
