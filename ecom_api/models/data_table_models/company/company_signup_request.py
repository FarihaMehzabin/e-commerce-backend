from flask_api import status

class CompanySignupRequestDataModel:
    def __init__(self, user):
        self.company = user.get("company_name")
        self.username = user.get("username")
        self.password = user.get("password")
        self.error_message = None
        self.status_code = status.HTTP_200_OK
        self.validate()

    def validate(self):
        try:
            if not self.username or not isinstance(self.username, str) or len(self.username) < 3:
                raise ValueError("Invalid username.")

            if not self.password or not isinstance(self.password, str) or len(self.password) < 8:
                raise ValueError("Invalid password. Password must be at least 8 characters.")
            
            if not self.company or not isinstance(self.company, str) or len(self.company) < 1:
                raise ValueError("Invalid company name.")
            
            
        except ValueError as e:
            self.error_message = str(e)
            self.status_code = status.HTTP_400_BAD_REQUEST
        
    
    