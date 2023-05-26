from ecom_api.services.db_functions import DbFunctions
from ecom_api.logger import Logger

class CategoryDB:
    def __init__(self):
        self.db = DbFunctions()
        self.logger = Logger()

    def get_all_categories(self):
        try:
            categories = self.db.fetch("SELECT * FROM Category")
            return categories
        except Exception as e:
            self.logger.error(f"Error fetching categories: {e}")
            raise

    def add_category(self, category):
        try:
            success, id = self.db.insert(f"INSERT INTO Category (name) VALUES (%s)", (category,))
            if success:
                self.logger.info("Category added successfully.")
                return True, id
            else:
                self.logger.warning("Failed to add category.")
                return False, 0
        except Exception as e:
            self.logger.error(f"Error adding category: {e}")
            raise

    def edit_category(self, old_category, new_category):
        try:
            result = self.db.edit(f'UPDATE Category SET name = "{new_category}" WHERE name = "{old_category}";')
            if result == "updated successfully":
                self.logger.info("Category edited successfully.")
                return True
            else:
                self.logger.warning("Failed to edit category. No matching record found.")
                return False
        except Exception as e:
            self.logger.error(f"Error editing category: {e}")
            raise

    def delete_category(self, category):
        try:
            result = self.db.delete(f'DELETE FROM Category WHERE name = "{category}";')
            if result == "deleted successfully":
                self.logger.info("Category deleted successfully.")
                return True
            else:
                self.logger.warning("Failed to delete category. No matching record found.")
                return False
        except Exception as e:
            self.logger.error(f"Error deleting category: {e}")
            raise
