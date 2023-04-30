from ecom_api.db.order_db import OrderDB
from ecom_api.db.product_db import ProductDB

class OrderService:
    def __init__(self) -> None:
        self.order_db = OrderDB()
        self.product_db = ProductDB()
    
    def create_order(self, order):
        result = self.order_db.insert_order_details_and_reserve(order)
        
        if result[0] == 0:
            return True, "Stock reservation successful"
        
        stock_out_product_details = self.product_db.get_product_by_id(result[1])
        
        return False,f"Stock reservation failed: insufficient stock for this item - {stock_out_product_details[0][1]} ", stock_out_product_details[0][1]
    
    