class CheckUserSessionResponseModel:
    def __init__(self, session_validity, username):
        self.session_validity = session_validity
        self.username = username