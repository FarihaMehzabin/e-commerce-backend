class CheckUserSessionResultDataModel:
    def __init__(self, session_valid, username, user_id):
        self.session_valid = session_valid
        self.username = username
        self.user_id = user_id
        
    def to_dict(self):
        return {"session_valid": self.session_valid, "username": self.username, "user_id": self.user_id}