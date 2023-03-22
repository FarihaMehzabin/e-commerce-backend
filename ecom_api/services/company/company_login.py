import traceback
from services.hashing import Hashing
from services.db_functions import DbFunctions
from models.data_table_models.company.company_login_result import CompanyLoginResultDataModel


class CompanyLoginService:
    def __init__(self):
        self.hash = Hashing()
        self.db = DbFunctions()
    
    
    def comp_login(self, company):

        res = self.db.fetch(f"SELECT * FROM company WHERE username = '{company.username}'")

        data = res[0]
        
        if data is not None:

            hash = data[3]
            
            response = CompanyLoginResultDataModel(self.hash.compare_pass(company.password, hash), data[0])

            return response

        return CompanyLoginResultDataModel(False, 1)
    
    