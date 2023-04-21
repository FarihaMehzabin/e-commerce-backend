from ecom_api.db.product_db import ProductDB
from ecom_api.models.data_table_models.company.product import ProductDataModel


class ProductService:
    def __init__(self):
        self.product_db = ProductDB()
    
    def get_products_by_company(self, id):
        
        data = self.product_db.get_products_by_company_id(id)
        
        if not data:
            return None
        
        products = [ProductDataModel(product).to_dict() for product in data]

        return {"products": products}


    def get_product_by_id(self, id):
        
        data = self.product_db.get_product_by_id(id)
        
        if not data:
            return None
        
        product = ProductDataModel(data[0]).to_dict()
        

        return {"product": product}

    
    def add_product(self, product_data, company_id):
        
        data = self.product_db.add_product(product_data, company_id)
        
        if not data:
            return None
        
        return {"message": "product added successfully"}
    
    def update_product(self, product_id, update_product_data):
        data = self.product_db.update_product(product_id, update_product_data)
        
        if not data:
            return None
        
        return {"message": "product updated successfully"}
    
    def delete_product(self, product_id):
        data = self.product_db.delete_product(product_id)
        
        if not data:
            return None
        
        return {"message": "product deleted successfully"}
