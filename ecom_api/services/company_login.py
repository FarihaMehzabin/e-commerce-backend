import traceback
from hashing import Hashing
from db_functions import DbFunctions
from models.data_table_models.return_company_login import ReturnCompanyLoginDataModel


class CompanyLoginService:
    def __init__(self):
        self.hash = Hashing()
        self.db = DbFunctions()
    
    
    def comp_login(self, company):

        res = self.db.fetch(f"SELECT * FROM company WHERE username = '{company.username}'")

        data = res[0]
        
        if data is not None:

            hash = data[3]
            
            response = ReturnCompanyLoginDataModel(self.hash.compare_pass(company.password, hash), data[0])

            return response

        return ReturnCompanyLoginDataModel(False, 1)
    
    