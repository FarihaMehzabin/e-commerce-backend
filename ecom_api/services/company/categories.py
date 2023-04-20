from ecom_api.db.company_db import CompanyDB


class CategoryService:
    
    def __init__(self) -> None:
        self.company_db = CompanyDB()
        
    def category_list(self):
        
        print("Fetching categories...")
        
        category_list = self.company_db.category_list()
        
        print(f"Category list: {category_list}")
        
        print("Done fetching categories.")
        
        return category_list
    
    # adding a new category to the category table 
    # returns the category id
    def add_category(self, category):
        
        inserted , id = self.company_db.add_category(category)
        
        if inserted: 
            return id
        
    def edit_category(self, old_category, new_category):
        
        message = self.company_db.edit_category(old_category, new_category)
    
        print(message)
        
        return message
    
    def delete_category(self, category):
        
        message = self.company_db.delete_category(category)
        
        return message