class UserLoginResponseModel:
    def __init__(self, user):
        self.message = user.message
        self.error = user.error
        
        
    def to_dict(self):
        return{
            "message": self.message,
            "error": self.error,
            
        }
    
    