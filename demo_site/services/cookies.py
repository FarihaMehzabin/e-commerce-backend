from flask import request, make_response, render_template, url_for
import requests


class Cookies:
    # Check if a cookie is present and valid, returning the username message and a boolean for cookie validity
    def check_cookie(self):
        cookie_check = self.get_cookie()

        message = "No session found"
        user_logged = False
        user_id = ""

        if cookie_check:
            cookie_validity, user_id = self.check_cookie_validity()

            if cookie_validity:
                message = cookie_validity.data.decode("utf-8")
                user_logged = True

        print(message, user_logged, user_id)

        return user_logged, message, user_id

    # Set a new cookie with the user_id as a parameter
    def set_cookie(self, user_id):
        data = requests.post(f"http://127.0.0.1:8081/user/create-session/{user_id}")
        res = data.json()
        response = make_response()
        response.set_cookie("session", res["guid"])
        return response

    # Check if a cookie is present in the request
    def get_cookie(self):
        name = request.cookies.get("session")
        if name is None:
            return False
        else:
            return True

    # Check if the cookie is valid, returning a response with the username message if valid, or False if not valid
    def check_cookie_validity(self):
        guid = request.cookies.get("session")
        data = requests.post(f"http://127.0.0.1:8081/user/check-cookie-validity/{guid}")
        res = data.json()

        if res["session_validity"] == True:
            return make_response(f"welcome {res['username']}"), res["user_id"]
        else:
            return False, ""

    # Return a cookie for the user, redirecting them to the index page
    def return_cookie(self, user_data):
        set_cookie = self.set_cookie(user_data.user_id)
        set_cookie.headers["location"] = url_for("index")
        return set_cookie, 302
