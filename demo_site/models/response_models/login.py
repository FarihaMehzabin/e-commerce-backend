class LoginResponseModel:
    # Initialize LoginResponseModel with a user object containing a message and user ID
    def __init__(self, user):
        self.message = user['message']
        self.user_id = user['user_id']