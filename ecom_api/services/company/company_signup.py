import traceback
from ecom_api.db.company_db import CompanyDB
from ecom_api.services.hashing import Hashing
from ecom_api.services.db_functions import DbFunctions
from ecom_api.models.data_table_models.company.company_signup_result import CompanySignupResultDataModel

class CompanySignupService:
    def __init__(self):
        self.hash = Hashing()
        self.company_db = CompanyDB()
    
    def comp_signup(self, company):

        try:

            rowcount, id = self.company_db.create_company_user(company)
            
            if rowcount:
        
                response = CompanySignupResultDataModel(rowcount, f"New user signed up! Welcome :) {company.username}", False , id)
            else:
                
                response = CompanySignupResultDataModel(False, "Username taken. Please try again.", True)

            return response
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

            