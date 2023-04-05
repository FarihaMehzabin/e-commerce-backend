class TemplateWithCookieData:
    def __init__(self, template, error, session_value, redirect_location):
        self.template = template
        self.error = error
        self.session_value = session_value
        self.redirect_location = redirect_location
