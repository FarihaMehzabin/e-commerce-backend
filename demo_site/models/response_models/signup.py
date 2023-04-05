class SignupResponseModel:
    def __init__(self, user):
        self.message = user['message']
        self.user_id = user['user_id']