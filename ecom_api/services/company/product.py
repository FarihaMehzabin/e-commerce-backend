from ecom_api.db.product_db import ProductDB
from ecom_api.models.data_table_models.company.product import ProductDataModel
from ecom_api.models.data_table_models.company.product_category import ProductCategoryDataModel
from ecom_api.db.application import Application
from ecom_api.logger import Logger

logger = Logger()

class ProductService:
    def __init__(self):
        self.product_db = ProductDB()
        self.cache = Application.instance()
        logger.info("ProductService Initialized")

    def get_all_products(self):
        try:
            product_data = self.product_db.get_all_products()
            logger.info("Fetched all products successfully")
        except Exception as e:
            logger.error(f"An error occurred while fetching products: {e}")
            return None

        products = {}
        for data in product_data:
            if data[0] not in products:
                try:
                    product = ProductDataModel(data)
                    category_name = self.cache.category_repository.get_category(data[8])
                    product.category_names.append(category_name)
                    products[product.product_id] = product.to_dict()
                except Exception as e:
                    logger.error(f"An error occurred while transforming product data: {e}")
                    return None
            else:
                category_name = self.cache.category_repository.get_category(data[8])
                products[data[0]]['category_names'].append(category_name)

        return {"products": products}

    def get_products_by_company(self, id):
        try:
            product_data = self.product_db.get_products_by_company_id(id)
            logger.info(f"Fetched products for company id: {id}")
        except Exception as e:
            logger.error(f"An error occurred while fetching products for company id: {id}: {e}")
            return None

        if not product_data:
            logger.warning(f"No product data found for company id: {id}")
            return None

        try:
            category_id = self.product_db.get_categories_by_company_id(id)
            product_category = [ProductCategoryDataModel(category).to_dict() for category in category_id]
            products = self._get_categories(product_category, product_data)
            logger.info(f"Fetched and transformed products for company id: {id}")
        except Exception as e:
            logger.error(f"An error occurred while fetching and transforming products for company id: {id}: {e}")
            return None

        return {"products": products}

    def get_product_by_id(self, id):
        try:
            data = self.product_db.get_product_by_id(id)
            logger.info(f"Fetched product with id: {id}")
        except Exception as e:
            logger.error(f"An error occurred while fetching product with id: {id}: {e}")
            return None

        if not data:
            logger.warning(f"No product data found for product id: {id}")
            return None

        try:
            category_id = self.product_db.get_categories_by_company_id(data[0][4])
            product_category = [ProductCategoryDataModel(category).to_dict() for category in category_id]
            product = self._get_categories(product_category,data)
            logger.info(f"Fetched and transformed product data for product id: {id}")
        except Exception as e:
            logger.error(f"An error occurred while fetching and transforming product data for product id: {id}: {e}")
            return None

        return {"product": product}

    def add_product(self, product_data, company_id):
        try:
            data, product_id = self.product_db.add_product(product_data, company_id)
            self.product_db.add_categories(product_id, product_data['selected_category_ids'])
            logger.info("Added product successfully")
        except Exception as e:
            logger.error(f"An error occurred while adding product: {e}")
            return None

        if not data:
            logger.warning("No product data found after attempting to add product")
            return None

        return {"message": "product added successfully"}

    def update_product(self, product_id, update_product_data):
        try:
            data = self.product_db.update_product(product_id, update_product_data)
            self.product_db.update_categories(product_id, update_product_data['selected_category_ids'])
            logger.info(f"Updated product with id: {product_id}")
        except Exception as e:
            logger.error(f"An error occurred while updating product with id: {product_id}: {e}")
            return None

        if not data:
            logger.warning(f"No product data found for product id: {product_id} after attempting to update product")
            return None

        return {"message": "product updated successfully"}

    def delete_product(self, product_id):
        try:
            data = self.product_db.delete_product(product_id)
            logger.info(f"Deleted product with id: {product_id}")
        except Exception as e:
            logger.error(f"An error occurred while deleting product with id: {product_id}: {e}")
            return None

        if not data:
            logger.warning(f"No product data found for product id: {product_id} after attempting to delete product")
            return None

        return {"message": "product deleted successfully"}

    def _get_categories(self, category_data, product_data):
        products = []
        for data in product_data:
            try:
                product = ProductDataModel(data)
                for pc in category_data:
                    if pc["product_id"] == product.product_id:
                        product.category_ids.append(pc["category_id"])
                        product.category_names.append(self.cache.category_repository.get_category(pc["category_id"]))
                products.append(product.to_dict())
                logger.info("Fetched and transformed categories successfully")
            except Exception as e:
                logger.error(f"An error occurred while fetching and transforming categories: {e}")
                return None

        return products
