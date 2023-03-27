class UserSignupResultDataModel:
    def __init__(self, user_created, message, error, user_id = 0):
        self.user_created = user_created
        self.user_id = user_id
        self.message = message
        self.error = error