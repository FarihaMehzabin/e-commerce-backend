from flask import request, make_response, render_template, url_for
import requests


class Cookies:
    def check_cookie(self):
        cookie_check = self.get_cookie()

        message = ""
        err_message = ""
        company_id = ""

        if cookie_check:
            cookie_validity, company_id = self.check_cookie_validity()

            if cookie_validity:
                message = cookie_validity.data.decode("utf-8")
                err_message = True

            else:
                err_message = False

        return message, err_message, company_id

    def set_cookie(self, comp_id):
        data = requests.post(f"http://127.0.0.1:8081/company/create-session/{comp_id}")

        res = data.json()

        response = make_response()

        response.set_cookie("session", res["guid"])

        return response

    def get_cookie(self):
        name = request.cookies.get("session")

        if name is None:
            return False

        else:
            return True

    def check_cookie_validity(self):
        guid = request.cookies.get("session")

        data = requests.post(
            f"http://127.0.0.1:8081/company/check-cookie-validity/{guid}"
        )

        res = data.json()

        if res["session_validity"] == True:
            return make_response(f"{res['company_name']}"), res["company_id"]
        else:
            return False

    def return_cookie(self, user_data):
        set_cookie = self.set_cookie(user_data.company_id)

        set_cookie.headers["location"] = url_for("index")

        return set_cookie, 302
