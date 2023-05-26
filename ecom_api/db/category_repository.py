import time
from ecom_api.db.category_db import CategoryDB
from ecom_api.models.data_table_models.company.category import CategoryDataModel
from ecom_api.read_write_lock import ReadWriteLock
from ecom_api.logger import Logger

logger = Logger()

class CategoryRepository:
    def __init__(self):
        self.categories = {}
        self.lock = ReadWriteLock()
        self.last_loaded = None
        self.category_db = CategoryDB()

    def get_category(self, id):
        now = time.time()

        if len(self.categories) == 0 or now - self.last_loaded > 20:
            self.lock.acquire_write()
            try:
                if len(self.categories) == 0 or now - self.last_loaded > 20:
                    self.last_loaded = time.time()

                    # Load the categories from the DB.
                    categories = self.category_db.get_all_categories()

                    # Clear the existing categories list.
                    self.categories.clear()

                    # Populate the categories list with new data.
                    category_list = [CategoryDataModel(category).to_dict() for category in categories]
                    for c in category_list:
                        self.categories[c['category_id']] = c['category_name']
                    
                    logger.info(f"Loaded {len(self.categories)} categories from database.")
            except Exception as e:
                logger.error(f"Error loading categories from database: {e}")
                raise
            finally:
                self.lock.release_write()

        self.lock.acquire_read()
        try:
            category = self.categories[id]
            logger.debug(f"Retrieved category '{category}' with id {id} from cache.")
        except KeyError:
            logger.error(f"Category with id {id} not found.")
            raise ValueError(f"Category with id {id} not found.")
        finally:
            self.lock.release_read()

        return category
