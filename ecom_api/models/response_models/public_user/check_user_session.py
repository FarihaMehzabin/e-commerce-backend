class CheckUserSessionResponseModel:
    def __init__(self, session_validity, username):
        self.session_validity = session_validity
        self.username = username

    def to_dict(self):
        return {"session_validity": self.session_validity, "username": self.username}
