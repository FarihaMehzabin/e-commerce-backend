from ecom_api.models.data_table_models.company.category import CategoryDataModel
from ecom_api.db.category_db import CategoryDB
from ecom_api.logger import Logger

logger = Logger()

class CategoryService:
    
    def __init__(self) -> None:
        self.category_db = CategoryDB()
        
    def category_list(self):
        try:
            category_data = self.category_db.get_all_categories()
            category_list = [CategoryDataModel(category).to_dict() for category in category_data]
            logger.info(f"Fetched {len(category_list)} categories.")
            return category_list
        except Exception as e:
            logger.error(f"Error fetching categories: {e}")
            raise
        
    # adding a new category to the category table 
    # returns the category id
    def add_category(self, category):
        try:
            success, category_id = self.category_db.add_category(category)
            if success:
                logger.info(f"Added category '{category}' with ID {category_id}.")
                return category_id
            else:
                logger.warning(f"Failed to add category '{category}': Category may already exist.")
                return None
        except Exception as e:
            logger.error(f"Error adding category '{category}': {e}")
            raise
        
    def edit_category(self, old_category, new_category):
        try:
            success = self.category_db.edit_category(old_category, new_category)
            if success:
                logger.info(f"Edited category from '{old_category}' to '{new_category}'.")
                return "Category edited successfully."
            else:
                logger.warning(f"Failed to edit category '{old_category}': Category may not exist.")
                return "Failed to edit category."
        except Exception as e:
            logger.error(f"Error editing category from '{old_category}' to '{new_category}': {e}")
            raise
        
    def delete_category(self, category):
        try:
            success = self.category_db.delete_category(category)
            if success:
                logger.info(f"Deleted category '{category}'.")
                return "Category deleted successfully."
            else:
                logger.warning(f"Failed to delete category '{category}': Category may not exist.")
                return "Failed to delete category."
        except Exception as e:
            logger.error(f"Error deleting category '{category}': {e}")
            raise
