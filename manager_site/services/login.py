import requests
class LoginService:
    def __init__(self):
        pass
    
    def user_login(self, user):
        response = requests.post(
            f"http://127.0.0.1:8080/company/user/login",
            json={"username": user.username , "password": user.password}
        )

        res = response.json()
        
        return res