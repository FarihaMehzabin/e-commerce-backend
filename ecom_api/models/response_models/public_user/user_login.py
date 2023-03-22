class UserLoginResponseModel:
    def __init__(self, message, error, user_id):
        self.message = message
        self.error = error
        self.user_id = user_id
    
    