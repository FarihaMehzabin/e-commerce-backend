import requests

class SignupService:
    
    def create_user(self, user):
        response = requests.post(
            f"http://127.0.0.1:8080/company/user/signup",
            json={"company_name":user.company_name, "username": user.username , "password": user.password}
        )

        res = response.json()
        
        return res