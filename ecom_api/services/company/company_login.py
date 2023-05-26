import traceback
from ecom_api.db.company_db import CompanyDB
from ecom_api.services.hashing import Hashing
from ecom_api.models.data_table_models.company.company_login_result import CompanyLoginResultDataModel
from ecom_api.logger import Logger

class CompanyLoginService:
    def __init__(self):
        self.hash = Hashing()
        self.company_db = CompanyDB()
        self.logger = Logger()
    
    def comp_login(self, company):
        try:
            data = self.company_db.get_company_by_username(company.username)

            if data is not None:
                hash = data[3]
                response = CompanyLoginResultDataModel(self.hash.compare_pass(company.password, hash), f"Logged in! Welcome :) {company.username}", False,data[0])
                self.logger.info(f"Successful login attempt for company: {company.username}")
                return response

            self.logger.warning(f"Invalid login attempt for company: {company.username}")
            return CompanyLoginResultDataModel(False, "Invalid Credentials. Please try again.", True, 1)

        except Exception as e:
            self.logger.error(f"An error occurred during login for company: {company.username}. Error: {str(e)}")
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            self.logger.debug(f"Traceback for error: {traceback_str}")
            return CompanyLoginResultDataModel(False, "An unexpected error occurred. Please try again later.", True, 1)
