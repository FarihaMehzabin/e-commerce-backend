

class UserSignupRequestDataModel:
    def __init__(self, user):
        self.username = user["username"]
        self.password = user["password"]
        self.first_name = user["first_name"]
        self.last_name = user["last_name"]