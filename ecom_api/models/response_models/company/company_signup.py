class CompanySignupResponseModel:
    def __init__(self, company):
        self.message = company.message
        self.error = company.error
        self.company_id = company.company_id
    
    def to_dict(self):
        return {
            "message": self.message,
            "error": self.error,
            "company_id": self.company_id
        }
    