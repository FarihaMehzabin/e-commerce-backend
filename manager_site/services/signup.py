import requests


class SignupService:
    def create_user(self, user):
        response = requests.post(
            f"http://127.0.0.1:8081/company/user/signup",
            json={
                "company_name": user.company_name,
                "username": user.username,
                "password": user.password,
                "email": user.email,
            },
        )

        res = response.json()

        return res
