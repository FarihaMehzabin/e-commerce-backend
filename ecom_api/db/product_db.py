from services.db_functions import DbFunctions

class ProductDB:
    
    def __init__(self):
        self.db = DbFunctions()

    def get_products(self):
            data = self.db.fetch("SELECT product.name AS product_name, product.price AS price, (SELECT Category.name FROM Category WHERE Category.id = (SELECT product_category.category_id FROM product_category WHERE product_category.product_id = product.id)) AS category_name FROM product;")
            
            print(data)
            
            return data[0], data[1], data[2]