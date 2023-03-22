import uuid, traceback
from services.hashing import Hashing
from models.data_table_models.company.create_company_session_result import CreateCompanySessionResultDataModel
from models.data_table_models.company.check_company_session_result import CheckCompanySessionResultDataModel


class CompanySessionService:
    def __init__(self):
        self.hash = Hashing()
        
    def create_session(self, comp_id):
        guid_id = str(uuid.uuid4())
        
        hashed_guid = hash.hash_guid(guid_id)
        
        try:
            self.db.insert(
                f"INSERT INTO session (guid, company_id) VALUES (%s, %s)",
                (hashed_guid, comp_id),
            )
            
            response = CreateCompanySessionResultDataModel(hashed_guid)
            
            return response

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
        
    def check_session_comp(self, guid):

        res = self.db.fetch(
            f"SELECT guid, company_id FROM session WHERE guid = '{guid}'"
        )
        
        data = res[0]

        guid = data[0]

        comp_id = data[1]
        
        print(f"company id: {comp_id}")

        if comp_id is not None:

            res = self.db.fetch(f"SELECT name FROM company WHERE id = '{comp_id}'")
            
            data = res[0]
            
            if guid is not None:
                
                response = CheckCompanySessionResultDataModel(True, data[0])
                
                return response

        return CheckCompanySessionResultDataModel(False, "No company present")
        
        