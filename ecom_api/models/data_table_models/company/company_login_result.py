class CompanyLoginResultDataModel:
    def __init__(self, user_logged, message, error, company_id = 0):
        self.user_logged = user_logged
        self.company_id = company_id
        self.message = message
        self.error = error