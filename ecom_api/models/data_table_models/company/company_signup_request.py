

class CompanySignupRequestDataModel:
    def __init__(self, user):
        self.company = user["company_name"]
        self.username = user["username"]
        self.password = user["password"]
        
    
    