from ecom_api.services.db_functions import DbFunctions 
from ecom_api.services.hashing import Hashing
import traceback



class CompanyDB:
    def __init__(self):
        self.db = DbFunctions()
        self.hash = Hashing()

    # Get company by username
    def get_company_by_username(self, username):
        res = self.db.fetch(f"SELECT * FROM company WHERE username = '{username}'")
        return res[0] if res else None

    # Create a new company user with the provided company information
    def create_company_user(self, company):
        try:
            hashed_pass = self.hash.hash_pass(company.password)

            rowcount, id = self.db.insert(
                f"INSERT INTO company (name, username, password) VALUES (%s, %s, %s)",
                (company.company, company.username, hashed_pass),
            )
            return rowcount, id

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
            return None, None
    
    def add_category(self, category):
        res = self.db.insert(f"INSERT INTO Category (name) VALUES (%s)", (category,))   
        
        return res
    
    def edit_category(self, old_category, new_category):
        res = self.db.edit(f'UPDATE Category SET name = "{new_category}" WHERE name = "{old_category}";')
        
        return "Category edited successfully"
    
    def delete_category(self, category):
        res = self.db.delete(f'DELETE FROM Category WHERE name = "{category}";')
        
        return "Category deleted successfully"
        
        
    
