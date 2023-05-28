from flask.scaffold import F
from ecom_api.db.order_db import OrderDB
from ecom_api.db.product_db import ProductDB
from ecom_api.db.user_db import UserDB
from ecom_api.logger import Logger
from kafka import KafkaProducer
import json


logger = Logger()

class OrderService:
    def __init__(self) -> None:
        self.order_db = OrderDB()
        self.product_db = ProductDB()
        self.user_db = UserDB()
    
    def create_order(self, order):
        
        order_id = self.order_db.insert_order_details(order)
        
        logger.info(f"Order created. OrderID: {order_id}")
        
        result = self.order_db.reserve_stock(order)
        
        if result[0] == 0:
            
            logger.info(f"OrderID: {order_id}. Stock reserve successful.")
                        
            total_amount = sum(item["quantity"] * self.product_db.get_product_price_by_id(item["product_id"]) for item in order.items)
            
            logger.info(f"OrderID: {order_id}. Total amount: {total_amount}")
            
            return True, "Stock reservation successful", total_amount, order_id
        
        stock_out_product_details = self.product_db.get_product_by_id(result[1])
        
        logger.warning(f"OrderID: {order_id}. Stock reservation not successful. Stock out product: {stock_out_product_details[0][1]}")
        
        return False,f"Stock reservation failed: insufficient stock for this item - {stock_out_product_details[0][1]} ", stock_out_product_details[0][1], order_id
    
    
    
    def process_paid_orders_reservations(self, user_id, order_id):
        
        result = self.order_db.process_paid_orders(user_id, order_id)
        
        if result[0] == -1:
            
            logger.warning(f"Failed processing order. OrderID: {order_id}")
            
            update_product_stock_result = self.order_db.update_product_stock(user_id, order_id)
            
            if update_product_stock_result[0] == -1:
                
                logger.debug(update_product_stock_result)
                                
                stock_out_product_details = self.product_db.get_product_by_id(update_product_stock_result[1])
                
                logger.warning(f"Failed to regain stock. {stock_out_product_details[0][1]} got stock out. User needs refund. OrderID: {order_id}. User: {user_id}")
                
                return False, f"{stock_out_product_details[0][1]} got stock out. You will be refunded soon."
            
            logger.info(f"Order id: {order_id}. Successfully regained stock for the products and order is now processed.")
            
            return True,
        
        logger.info(f"Order id: {order_id}. Successfully processed order.")
        
        return True,
    
    def process_paid_orders_delivery(self, order_id, user_id):
        producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        
        user_data = self.user_db.get_user_by_id(user_id)
        
        logger.debug(user_data)
        
        email = user_data[7]
            
        producer.send('order-delivery', {'order_id': order_id, 'status': 'paid', 'user_id': user_id, 'email': email})
            