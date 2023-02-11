from flask import request, make_response, render_template
import requests

class cookies: 
    
    
    def _set_cookie(self):
        
        data = requests.get(f"http://127.0.0.1:8080/generate_and_store_GUID")
            
        res = data.json()
        
        response = make_response()
        
        response.set_cookie('session', res['guid'] )
        
        return response
    
    def check_for_cookie(self):
        name = request.cookies.get('session')
        
        print(name)
        
        # no cookie exists. Generate a new one
        
        if name is None:
            return self._set_cookie()
            
        else:
            return self._check_cookie_validity(name)
    
    def _check_cookie_validity(self, guid):
        data = requests.get(f"http://127.0.0.1:8080/check_cookie_validity/{guid}")
            
        res = data.json()
        
        if res['check'] == True:
            return make_response("welcome")
        else:
            return self._set_cookie()
        
    