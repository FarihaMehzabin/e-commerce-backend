
class ProductCategoryDataModel:
    def __init__(self, data):
        self.id = data[0]
        self.product_id = data[1]
        self.category_id = data[2]
        
    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "category_id": self.category_id,
        }
