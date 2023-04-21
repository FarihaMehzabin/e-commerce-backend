class ProductDataModel:
    def __init__(self, product_tuple):
        self.product_id = product_tuple[0]
        self.product_name = product_tuple[1]
        self.product_price = product_tuple[2]
        self.product_description = product_tuple[3]
        self.company_id = product_tuple[4]
        self.unit = product_tuple[5]
        self.weight = product_tuple[6]
        self.brand = product_tuple[7]
        

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_price": self.product_price,
            "company_id": self.company_id,
            "unit": self.unit,
            "weight": self.weight,
            "brand": self.brand,
            "description": self.product_description
        }
