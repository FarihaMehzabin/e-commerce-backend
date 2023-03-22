import traceback
from services.hashing import Hashing
from services.db_functions import DbFunctions
from models.data_table_models.company.company_signup_result import CompanySignupResultDataModel

class CompanySignupService:
    def __init__(self):
        self.hash = Hashing()
        self.db = DbFunctions()
    
    def comp_signup(self, company):

        try:

            hashed_pass = self.hash.hash_pass(company.password)

            rowcount, id = self.db.insert(
                f"INSERT INTO company (name, username, password) VALUES (%s, %s, %s)",
                (company.company, company.username, hashed_pass),
            )
        
            response = CompanySignupResultDataModel(rowcount, id)

            return response
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

            return CompanySignupResultDataModel(False, 1)