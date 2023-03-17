from flask import request, make_response, render_template, url_for
import requests


class cookies:
    
    def check_cookie(self):
        cookie_check = self.get_cookie()
        
        message = ""
        err_message = ""

        print(cookie_check)

        if cookie_check:
            
            cookie_validity = self.check_cookie_validity()
            
            if cookie_validity:
                
                message = cookie_validity.data.decode('utf-8') 
                err_message = False
                
            else:
                err_message = "❌ you're not logged in"

        return message, err_message
    
    
    def check_cookie_with_redirect(self, location):
        cookie_check = self.get_cookie()

        if cookie_check:
            
            cookie_validity = self.check_cookie_validity()
            
            if cookie_validity:

                cookie_validity.headers["location"] = url_for(location)

                return cookie_validity, 302
            
            return False
        
        return False
    
    def set_cookie(self, comp_id):

        data = requests.get(f"http://127.0.0.1:8080/company/create-session/{comp_id}")

        res = data.json()

        response = make_response()

        response.set_cookie("session", res["guid"])

        return response

    def get_cookie(self):
        name = request.cookies.get("session")

        print(name)

        if name is None:

            return False

        else:
            return True

    def check_cookie_validity(self):
        
        guid = request.cookies.get("session")
        
        data = requests.get(f"http://127.0.0.1:8080/company/check-cookie-validity/{guid}")

        res = data.json()

        print(res)

        if res["check"] == True:
            return make_response(f"welcome {res['comp']}")
        else:
            return False
