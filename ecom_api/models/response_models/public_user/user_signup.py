class UserSignupResponseModel:
    def __init__(self, user):
        self.message = user.message
        self.error = user.error
        self.user_id = user.user_id
        
        
    def to_dict(self):
        return {"message": self.message, "error": self.error, "user_id": self.user_id}
    