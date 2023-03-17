import traceback
from hashing import Hashing
from db_functions import DbFunctions
from models.data_table_models.return_company_signup import ReturnCompanySignupDataModel

class CompanySignupService:
    def __init__(self):
        pass
    
    def comp_signup(self, company):

        try:

            hashed_pass = self.hash.hash_pass(company.password)

            rowcount, id = self.db.insert(
                f"INSERT INTO company (name, username, password) VALUES (%s, %s, %s)",
                (company.company, company.username, hashed_pass),
            )
        
            response = ReturnCompanySignupDataModel(rowcount, id)

            return response
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

            return ReturnCompanySignupDataModel(False, 1)