from ecom_api.services.db_functions import DbFunctions
import json

class OrderDB:
    def __init__(self) -> None:
        self.db = DbFunctions()
        
        
    def insert_order_details_and_reserve(self, order):
        result = self.db.call_proc("insert_order_and_items", (order.user_id, order.address_line_1, order.city, order.postcode, json.dumps(order.items)))
        
        if result:
            message = self._reserve_stock(order)
        
        return message
        
    def _reserve_stock(self, order):
        result = self.db.call_proc_with_result('reserve_stock', (order.user_id, json.dumps(order.items),))
        
        return result
    
    def delete_reservations(self, user_id):
        
        result = self.db.call_proc_with_result('delete_reservations', (user_id,))
        
        return result