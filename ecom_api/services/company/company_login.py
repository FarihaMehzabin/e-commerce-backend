import traceback
from ecom_api.db.company_db import CompanyDB
from ecom_api.services.hashing import Hashing

from ecom_api.models.data_table_models.company.company_login_result import CompanyLoginResultDataModel


class CompanyLoginService:
    def __init__(self):
        self.hash = Hashing()
        self.company_db = CompanyDB()
    
    
    def comp_login(self, company):

        data = self.company_db.get_company_by_username(company.username)
        
        if data is not None:

            hash = data[3]
            
            response = CompanyLoginResultDataModel(self.hash.compare_pass(company.password, hash), f"Logged in! Welcome :) {company.username}", False,data[0])

            return response

        return CompanyLoginResultDataModel(False, "Invalid Credentials. Please try again.", True, 1)
    
    