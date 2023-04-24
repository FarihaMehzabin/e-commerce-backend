
class CategoryDataModel:
    def __init__(self, data) -> None:
        self.category_id = data[0]
        self.category_name = data[1]
        
    def to_dict(self):
        return {
            "category_id": self.category_id,
            "category_name": self.category_name
        }