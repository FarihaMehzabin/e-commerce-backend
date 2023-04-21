class CheckCompanySessionResponseModel:
    def __init__(self, session_validity, company_name, company_id):
        self.session_validity = session_validity
        self.company_name = company_name
        self.company_id = company_id
        
    def to_dict(self):
        return {
            "session_validity":  self.session_validity ,
        "company_name": self.company_name, 
        "company_id": self.company_id 
        }