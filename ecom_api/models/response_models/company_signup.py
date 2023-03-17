class CompanySignupResponseModel:
    def __init__(self, message, error, company_id):
        self.message = message
        self.error = error
        self.company_id = company_id
    
    