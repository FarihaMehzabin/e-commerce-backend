class LoginResponseModel:
    def __init__(self, user):
        self.message = user['message']
        self.company_id = user['company_id']