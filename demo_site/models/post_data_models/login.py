class LoginPostModel:
    # Initialize LoginPostModel with username and password
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Convert the instance to a dictionary for easy processing
    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password
        }
