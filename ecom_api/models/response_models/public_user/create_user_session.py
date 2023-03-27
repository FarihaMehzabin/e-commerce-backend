class CreateUserSessionResponseModel:
    def __init__(self, guid):
        self.guid = guid
        
    def to_dict(self):
        return {'guid': self.guid}