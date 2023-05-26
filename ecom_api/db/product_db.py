from ecom_api.services.db_functions import DbFunctions
from ecom_api.logger import Logger

class ProductDB:
    def __init__(self):
        self.db = DbFunctions()
        self.logger = Logger()

    def get_all_products(self):
        try:
            data = self.db.call_proc_fetch("get_all_products_with_categories")
            self.logger.info("Retrieved all products successfully.")
            return data
        except Exception as e:
            self.logger.error(f"Error retrieving all products: {e}")
            raise

    def get_products_by_company_id(self, company_id):
        try:
            data = self.db.fetch(f"SELECT * FROM product WHERE company_id = {company_id}")
            self.logger.info(f"Retrieved products for company ID: {company_id} successfully.")
            return data
        except Exception as e:
            self.logger.error(f"Error retrieving products for company ID: {company_id}. Error: {e}")
            raise

    def get_categories_by_company_id(self, company_id):
        try:
            data = self.db.fetch(f"SELECT * FROM product_category pc WHERE pc.product_id IN (SELECT p.id FROM product p WHERE company_id = {company_id})")
            self.logger.info(f"Retrieved categories for company ID: {company_id} successfully.")
            return data
        except Exception as e:
            self.logger.error(f"Error retrieving categories for company ID: {company_id}. Error: {e}")
            raise

    def get_product_by_id(self, id):
        try:
            data = self.db.fetch(f"SELECT * FROM product WHERE id = {id}")
            self.logger.info(f"Retrieved product ID: {id} successfully.")
            return data
        except Exception as e:
            self.logger.error(f"Error retrieving product ID: {id}. Error: {e}")
            raise

    def get_product_price_by_id(self, id):
        try:
            data = self.db.fetch(f"SELECT price FROM product WHERE id = {id}")
            self.logger.info(f"Retrieved price for product ID: {id} successfully.")
            return data[0][0]
        except Exception as e:
            self.logger.error(f"Error retrieving price for product ID: {id}. Error: {e}")
            raise

    def add_product(self, product_data, company_id):
        try:
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

            result = self.db.insert(sql, values)
            self.logger.info("Product added successfully.")
            return result
        except Exception as e:
            self.logger.error(f"Error adding product. Error: {e}")
            raise

    def update_product(self, product_id, product_data):
        try:
            statement = f"""
                UPDATE product
                SET name = '{product_data["name"]}', brand = '{product_data["brand"]}', price = {product_data["price"]}, unit = {product_data["unit"]}, item_weight = '{product_data["item_weight"]}', product_description = '{product_data["product_description"]}'
                WHERE id = {product_id}
            """

            result = self.db.edit(statement)
            self.logger.info(f"Product ID: {product_id} updated successfully.")
            return result
        except Exception as e:
            self.logger.error(f"Error updating product ID: {product_id}. Error: {e}")
            raise

    def delete_product(self, product_id):
        try:
            statement = f"DELETE FROM product WHERE id = {product_id}"
            result = self.db.delete(statement)
            self.logger.info(f"Product ID: {product_id} deleted successfully.")
            return result
        except Exception as e:
            self.logger.error(f"Error deleting product ID: {product_id}. Error: {e}")
            raise

    def update_categories(self, product_id, category_ids):
        try:
            category_ids_str = ','.join(map(str, category_ids))
            self.db.call_proc("update_product_categories", (product_id, category_ids_str))
            self.logger.info(f"Categories updated successfully for product ID: {product_id}.")
        except Exception as e:
            self.logger.error(f"Error updating categories for product ID: {product_id}. Error: {e}")
            raise

    def add_categories(self, product_id, category_ids):
        try:
            category_ids_str = ','.join(map(str, category_ids))
            self.db.call_proc("add_product_categories", (product_id, category_ids_str))
            self.logger.info(f"Categories added successfully for product ID: {product_id}.")
        except Exception as e:
            self.logger.error(f"Error adding categories for product ID: {product_id}. Error: {e}")
            raise
