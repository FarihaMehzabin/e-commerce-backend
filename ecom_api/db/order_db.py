from ecom_api.services.db_functions import DbFunctions
from ecom_api.logger import Logger
import json

class OrderDB:
    def __init__(self) -> None:
        self.db = DbFunctions()
        self.logger = Logger()

    def insert_order_details(self, order):
        try:
            result = self.db.call_proc_with_result("insert_order_and_items", (order.user_id, order.address_line_1, order.city, order.postcode, json.dumps(order.items)))
            order_id = result[0][0]
            self.logger.info(f"Order details inserted successfully for order ID: {order_id}")
            return order_id
        except Exception as e:
            self.logger.error(f"Error inserting order details: {e}")
            raise

    def reserve_stock(self, order):
        try:
            result = self.db.call_proc_with_result('reserve_stock', (order.user_id, json.dumps(order.items),))
            return result[0]
        except Exception as e:
            self.logger.error(f"Error reserving stock: {e}")
            raise

    def process_paid_orders(self, user_id, order_id):
        try:
            process_paid_orders_result = self.db.call_proc_with_result('process_paid_orders', (user_id, order_id))
                                    
            return process_paid_orders_result[0]
        except Exception as e:
            self.logger.error(f"Error processing paid orders: {e}")
            raise

    def update_product_stock(self, user_id, order_id):
        try:
            update_product_stock_result = self.db.call_proc_with_result('update_product_stock', (user_id, order_id))
            return update_product_stock_result[0]
        except Exception as e:
            self.logger.error(f"Error updating product stock: {e}")
            raise
