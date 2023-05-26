import uuid, traceback
from ecom_api.services.hashing import Hashing
from ecom_api.models.data_table_models.company.create_company_session_result import CreateCompanySessionResultDataModel
from ecom_api.models.data_table_models.company.check_company_session_result import CheckCompanySessionResultDataModel
from ecom_api.db.company_session_db import CompanySessionDB
from ecom_api.logger import Logger

class CompanySessionService:
    def __init__(self):
        self.hash = Hashing()
        self.company_session_db = CompanySessionDB()
        self.logger = Logger()
        
    def create_session(self, comp_id):
        try:
            guid_id = str(uuid.uuid4())
            hashed_guid = self.hash.hash_guid(guid_id)
        
            if self.company_session_db.create_session(hashed_guid, comp_id): 
                self.logger.info(f"New session created for company id: {comp_id}")
                return CreateCompanySessionResultDataModel(hashed_guid)
            else:
                self.logger.warning(f"Session creation failed for company id: {comp_id}")
                return False
        except Exception as e:
            self.logger.error(f"Error in creating session for company id: {comp_id}. Error: {str(e)}")
            return False

        
    def check_session_comp(self, guid):
        try:
            data = self.company_session_db.get_session_by_guid(guid)

            if data:
                comp_id = data[1]
                self.logger.info(f"Checked session for company id: {comp_id}")
                
                res = self.company_session_db.get_user_by_id(comp_id)
                company_name = res[0]
                
                return CheckCompanySessionResultDataModel(True, company_name, comp_id)

            self.logger.warning(f"Invalid session guid: {guid}")
            return CheckCompanySessionResultDataModel(False, "No company present")
        except Exception as e:
            self.logger.error(f"Error in checking session for guid: {guid}. Error: {str(e)}")
            return CheckCompanySessionResultDataModel(False, "An error occurred")
