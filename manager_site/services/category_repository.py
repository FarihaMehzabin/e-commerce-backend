import time, requests
from manager_site.services.read_write_lock import ReadWriteLock


class CategoryRepository:
    def __init__(self):
        self.categories = []
        self.lock = ReadWriteLock()
        self.last_loaded = None

    def get_categories(self):
        now = time.time()

        if len(self.categories) == 0 or now - self.last_loaded > (20):
            self.lock.acquire_write()
            try:
                if len(self.categories) == 0 or now - self.last_loaded > (20):
                    self.last_loaded = time.time()

                    category_list_response = requests.get(
                        f"http://127.0.0.1:8081/company/categories"
                    )

                    category_list = category_list_response.json()

                    # Clear the existing categories list.
                    self.categories.clear()

                    for c in category_list["category_list"]:
                        self.categories.append((c["category_id"], c["category_name"]))

                    return self.categories
            finally:
                self.lock.release_write()
        else:
            self.lock.acquire_read()
            try:
                category = self.categories
            finally:
                self.lock.release_read()
            return category
