class CompanySignupResultDataModel:
    def __init__(self, user_created, message, error, company_id = 0):
        self.user_created = user_created
        self.company_id = company_id
        self.message = message
        self.error = error
        