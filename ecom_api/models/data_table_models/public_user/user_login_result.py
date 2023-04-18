from dataclasses import dataclass



class UserLoginResultDataModel:
    def __init__(self, user_logged, message, error, user_id = 0):
        self.user_logged = user_logged
        self.user_id = user_id
        self.message = message
        self.error = error