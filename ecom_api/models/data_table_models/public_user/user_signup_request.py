from email_validator import validate_email, EmailNotValidError

class UserSignupRequestDataModel:
    def __init__(self, user):
        self.username = user.get("username")
        self.password = user.get("password")
        self.first_name = user.get("first_name")
        self.last_name = user.get("last_name")
        self.email = user.get("email")
        self.error_message = None
        self.validate()

    def validate(self):
        try:
            if not self.username or not isinstance(self.username, str) or len(self.username) < 3:
                raise ValueError("Invalid username.")

            if not self.password or not isinstance(self.password, str) or len(self.password) < 8:
                raise ValueError("Invalid password. Password must be at least 8 characters.")
            
            if not self.first_name or not isinstance(self.first_name, str) or len(self.first_name) < 1:
                raise ValueError("Invalid first name.")
            
            if not self.last_name or not isinstance(self.last_name, str) or len(self.last_name) < 1:
                raise ValueError("Invalid last name.")

            try:
                v = validate_email(self.email) # validate and get info
                email = v["email"] # replace with normalized form
            except EmailNotValidError as e:
                # email is not valid, exception message is human-readable
                raise ValueError(str(e))

        except ValueError as e:
            self.error_message = str(e)
            
    def isValid(self):
        return self.error_message is None
