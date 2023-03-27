class CheckCompanySessionResponseModel:
    def __init__(self, session_validity, company_name):
        self.session_validity = session_validity
        self.company_name = company_name
        
    def to_dict(self):
        return {
            "session_validity":  self.session_validity ,
        "company_name": self.company_name 
        }