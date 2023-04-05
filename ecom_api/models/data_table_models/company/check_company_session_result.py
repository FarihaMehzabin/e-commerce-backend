class CheckCompanySessionResultDataModel:
    def __init__(self, session_valid, company_name):
        self.session_valid = session_valid
        self.company_name = company_name
    
    def to_dict(self):
        return {"session_valid": self.session_valid, "company_name": self.company_name}