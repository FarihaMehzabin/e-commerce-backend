import uuid, traceback
from services.hashing import Hashing
from models.data_table_models.company.create_company_session_result import CreateCompanySessionResultDataModel
from models.data_table_models.company.check_company_session_result import CheckCompanySessionResultDataModel
from db.company_session_db import CompanySessionDB

class CompanySessionService:
    def __init__(self):
        self.hash = Hashing()
        self.company_session_db = CompanySessionDB()
        
    def create_session(self, comp_id):
        guid_id = str(uuid.uuid4())
        
        hashed_guid = self.hash.hash_guid(guid_id)
        
        if self.company_session_db.create_session(hashed_guid, comp_id): 
            response = CreateCompanySessionResultDataModel(hashed_guid)
            return response
        else:
            return False

        
    def check_session_comp(self, guid):
        
        data = self.company_session_db.get_session_by_guid(guid)

        if data:
            comp_id = data[1]
            
            print(f"company id: {comp_id}")

            if comp_id is not None:

                res = self.company_session_db.get_user_by_id(comp_id)
                
                data = res[0]
                
                response = CheckCompanySessionResultDataModel(True, data)
                    
                return response

        return CheckCompanySessionResultDataModel(False, "No company present")
        
        