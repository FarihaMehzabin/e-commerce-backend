class CheckUserSessionResponseModel:
    def __init__(self, session_validity, username, user_id):
        self.session_validity = session_validity
        self.username = username
        self.user_id = user_id
        
    def to_dict(self):
        return {"session_validity": self.session_validity, "username": self.username, "user_id": self.user_id}
