import requests

class SignupService:
    
    def create_user(self, user):
        response = requests.post(
            f"http://127.0.0.1:8080/user-signup",
            json={"first_name":user.first_name,"last_name":user.last_name, "username": user.username , "password": user.password}
        )

        res = response.json()
        
        return res