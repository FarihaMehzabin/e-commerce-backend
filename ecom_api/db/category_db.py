from ecom_api.services.db_functions import DbFunctions

class CategoryDB:
    def __init__(self):
        self.db = DbFunctions()
        
    def get_all_categories(self):
        categories = self.db.fetch("SELECT * FROM Category")
        
        return categories