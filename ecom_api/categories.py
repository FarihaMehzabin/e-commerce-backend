from db_functions import DbFunctions

class Category:
    def __init__(self):
        self.db = DbFunctions()
        
    def category_list(self):
        
        print("Fetching categories...")
        
        category_list = self.db.fetch("SELECT name FROM Category")
        
        print(f"Category list: {category_list}")
        
        print("Done fetching categories.")
        
        return category_list
    
    # adding a new category to the category table 
    # returns the category id
    def add_category(self, category):
        inserted , id = self.db.insert(f"INSERT INTO Category (name) VALUES (%s)", (category,))   
        
        if inserted: 
            return id
        
    def edit_category(self, category_name, new_category_name):
        message = self.db.edit(f'UPDATE Category SET name = "{new_category_name}" WHERE name = "{category_name}";')
        
        print(message)
        
        return message