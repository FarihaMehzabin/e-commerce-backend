
class CompanyLoginResponseModel:
    def __init__(self, company):
        self.message = company.message
        self.error = company.error
        
    def to_dict(self):
        return {
            "message": self.message,
            "error": self.error,
        }
    
    