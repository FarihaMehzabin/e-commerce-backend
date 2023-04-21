class CheckCompanySessionResultDataModel:
    def __init__(self, session_valid, company_name, company_id = None):
        self.session_valid = session_valid
        self.company_name = company_name
        self.company_id = company_id
    
    def to_dict(self):
        return {"session_valid": self.session_valid, "company_name": self.company_name, "company_id": self.company_id}