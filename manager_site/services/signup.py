import requests
from models.post_data_models.signup import SignupPostModel

class SignupService:
    
    def create_user(self, user):
        response = requests.get(
            f"http://127.0.0.1:8080/company/user/signup/{user.company_name}/{user.username}/{user.password}"
        )

        res = response.json()