from ecom_api.db.order_db import OrderDB
from ecom_api.db.product_db import ProductDB

class OrderService:
    def __init__(self) -> None:
        self.order_db = OrderDB()
        self.product_db = ProductDB()
    
    def create_order(self, order):
        result, order_id = self.order_db.insert_order_details_and_reserve(order)
        
        print(f"order id: {order_id}")
        
        if result[0] == 0:
            total_amount = sum(item["quantity"] * self.product_db.get_product_price_by_id(item["product_id"]) for item in order.items)
            return True, "Stock reservation successful", total_amount, order_id
        
        stock_out_product_details = self.product_db.get_product_by_id(result[1])
        
        return False,f"Stock reservation failed: insufficient stock for this item - {stock_out_product_details[0][1]} ", stock_out_product_details[0][1], order_id
    
    def delete_reservations(self, user_id, order_id):
        
        result = self.order_db.delete_reservations(user_id, order_id)
        
        if result[0] == -1:
            stock_out_product_details = self.product_db.get_product_by_id(result[1])
            return False, f"{stock_out_product_details[0][1]} got stock out. You will be refunded soon."
        
        return True,