import traceback
from ecom_api.db.company_db import CompanyDB
from ecom_api.services.hashing import Hashing
from ecom_api.services.db_functions import DbFunctions
from ecom_api.models.data_table_models.company.company_signup_result import CompanySignupResultDataModel
from ecom_api.logger import Logger

class CompanySignupService:
    def __init__(self):
        self.hash = Hashing()
        self.company_db = CompanyDB()
        self.logger = Logger()
    
    def comp_signup(self, company):
        try:
            rowcount, id = self.company_db.create_company_user(company)
            
            if rowcount:
                response = CompanySignupResultDataModel(rowcount, f"New user signed up! Welcome :) {company.username}", False , id)
                self.logger.info(f"New company user signed up: {company.username}")
                return response
            else:
                self.logger.warning(f"Attempted signup with existing username: {company.username}")
                return CompanySignupResultDataModel(False, "Username taken. Please try again.", True)
        except Exception as err:
            traceback_str = ''.join(traceback.format_tb(err.__traceback__))
            self.logger.error(f"An error occurred during signup for company: {company.username}. Error: {str(err)}")
            self.logger.debug(f"Traceback for error: {traceback_str}")
            return CompanySignupResultDataModel(False, "An unexpected error occurred. Please try again later.", True)
