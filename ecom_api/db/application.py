from ecom_api.db.category_repository import CategoryRepository

class Application:
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._instance:
            raise RuntimeError("Use Application.instance() instead of creating a new instance.")
        self.category_repository = CategoryRepository()
        


