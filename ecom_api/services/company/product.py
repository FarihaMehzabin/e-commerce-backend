from unicodedata import category
from ecom_api.db.product_db import ProductDB
from ecom_api.models.data_table_models.company.product import ProductDataModel
from ecom_api.models.data_table_models.company.product_category import ProductCategoryDataModel
from ecom_api.db.application import Application
from ecom_api.logger import Logger
from ecom_api.routes import products

class ProductService:
    def __init__(self):
        self.product_db = ProductDB()
        self.cache = Application.instance()
        self.logger = Logger("ProductService")
    
    
    def get_all_products(self):
        product_data = self.product_db.get_all_products()
        
        products = {}
        
        for data in product_data:
            
            if data[0] not in products:
                product = ProductDataModel(data)
                
                category_name = self.cache.category_repository.get_category(data[8])
                
                product.category_names.append(category_name)
                
                products[product.product_id] = product.to_dict()
            else:
                category_name = self.cache.category_repository.get_category(data[8])
                
                products[data[0]]['category_names'].append(category_name)
            
        return {"products": products}
        
    
    def get_products_by_company(self, id):
        
        product_data = self.product_db.get_products_by_company_id(id)
        
        if not product_data:
            return None
        
        category_id = self.product_db.get_categories_by_company_id(id)
        
        product_category = [ProductCategoryDataModel(category).to_dict() for category in category_id]
            
        products = self._get_categories(product_category, product_data)
        
        return {"products": products}


    def get_product_by_id(self, id):
        
        data = self.product_db.get_product_by_id(id)
        
        if not data:
            return None
        
        category_id = self.product_db.get_categories_by_company_id(data[0][4])
        
        product_category = [ProductCategoryDataModel(category).to_dict() for category in category_id]
        
        product = self._get_categories(product_category,data)
        
        return {"product": product}

    
    def add_product(self, product_data, company_id):
        
        data, product_id = self.product_db.add_product(product_data, company_id)
        
        self.product_db.add_categories(product_id, product_data['selected_category_ids'])
        
        if not data:
            return None
        
        return {"message": "product added successfully"}
    
    
    def update_product(self, product_id, update_product_data):
        data = self.product_db.update_product(product_id, update_product_data)
        
        self.product_db.update_categories(product_id, update_product_data['selected_category_ids'])
        
        if not data:
            return None
        
        return {"message": "product updated successfully"}
    
    
    def delete_product(self, product_id):
        data = self.product_db.delete_product(product_id)
        
        if not data:
            return None
        
        return {"message": "product deleted successfully"}
            
    
    def _get_categories(self, category_data, product_data):
        
        products = []
    
        for data in product_data:
            product = ProductDataModel(data)
            
            for pc in category_data:
                if pc["product_id"] == product.product_id:
                    product.category_ids.append(pc["category_id"])
                    product.category_names.append(self.cache.category_repository.get_category(pc["category_id"]))
            
            products.append(product.to_dict())
            
            
        return products
