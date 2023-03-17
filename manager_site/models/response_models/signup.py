



class SignupResponseModel:
    def __init__(self, message, error, comp_id = None):
        self.message = message
        self.error = error
        self.comp_id = comp_id