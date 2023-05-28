import requests


class LoginService:
    def __init__(self):
        pass

    # Attempt to log in the user with the provided username and password
    def user_login(self, user):
        # Send a POST request to the user-login API endpoint with the user's credentials
        response = requests.post(
            f"http://127.0.0.1:8081/user-login",
            json={"username": user.username, "password": user.password},
        )

        # Parse the JSON response
        res = response.json()

        # Return the parsed response
        return res
