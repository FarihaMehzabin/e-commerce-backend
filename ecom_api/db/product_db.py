from ecom_api.services.db_functions import DbFunctions

class ProductDB:
    def __init__(self):
        self.db = DbFunctions()

    # Get all products with their names, prices, and category names
    def get_all_products(self):
        data = self.db.call_proc_fetch("get_all_products_with_categories")

        return data
    
    def get_products_by_company_id(self, company_id):
        data = self.db.fetch(f"SELECT * FROM product WHERE company_id = {company_id}")

        return data
    
    def get_categories_by_company_id(self, company_id):
        data = self.db.fetch(f"SELECT * FROM product_category pc WHERE pc.product_id IN (SELECT p.id FROM product p WHERE company_id = {company_id})")
        
        return data
    
    def get_product_by_id(self, id):
        data = self.db.fetch(f"SELECT * FROM product WHERE id = {id}")

        return data
    
    def add_product(self, product_data, company_id):
        sql = """
            INSERT INTO product (company_id, name, brand, price, unit, item_weight, product_description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
    company_id,
    product_data["name"],
    product_data["brand"],
    product_data["price"],
    product_data["unit"],
    product_data["item_weight"],
    product_data["product_description"],
)

        
        return self.db.insert(sql, values)
    
    def update_product(self, product_id, product_data):
        statement = f"""
            UPDATE product
            SET name = '{product_data["name"]}', brand = '{product_data["brand"]}', price = {product_data["price"]}, unit = {product_data["unit"]}, item_weight = '{product_data["item_weight"]}', product_description = '{product_data["product_description"]}'
            WHERE id = {product_id}
        """

        result = self.db.edit(statement)
        
        return result
    
    def delete_product(self, product_id):
        statement = f"DELETE FROM product WHERE id = {product_id}"
        result = self.db.delete(statement)
        return result

        
    def update_categories(self, product_id, category_ids):
        
        category_ids_str = ','.join(map(str, category_ids))
        
        self.db.call_proc("update_product_categories", (product_id, category_ids_str))
        
    def add_categories(self, product_id, category_ids):
        category_ids_str = ','.join(map(str, category_ids))
        
        self.db.call_proc("add_product_categories", (product_id, category_ids_str))


        