import requests

class SignupService:
    # Create a new user with the provided user information
    def create_user(self, user):
        
        # Send a POST request to the user-signup API endpoint with the user's information
        response = requests.post(
            f"http://127.0.0.1:8080/user-signup",
            json={"first_name":user.first_name,"last_name":user.last_name, "username": user.username , "password": user.password}
        )

        # Parse the JSON response
        res = response.json()
        
        # Return the parsed response
        return res