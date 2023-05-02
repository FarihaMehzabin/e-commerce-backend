from ecom_api.services.db_functions import DbFunctions
import json

class OrderDB:
    def __init__(self) -> None:
        self.db = DbFunctions()
        
        
    def insert_order_details_and_reserve(self, order):
        result = self.db.call_proc_with_result("insert_order_and_items", (order.user_id, order.address_line_1, order.city, order.postcode, json.dumps(order.items)))
        
        message = self._reserve_stock(order)
        
        return message, result[0][0]
        
    def _reserve_stock(self, order):
        result = self.db.call_proc_with_result('reserve_stock', (order.user_id, json.dumps(order.items),))
        
        print(result)
        
        return result[0]
    
    def delete_reservations(self, user_id, order_id):
        
        check_reservations_result = self.db.call_proc_with_result('check_reservations', (user_id, order_id))
        
        print("delete reservations")
        
        print(check_reservations_result)
        
        if check_reservations_result[0][0] == -1:
            result = self.db.call_proc_with_result('check_for_products_without_reservations', (user_id, order_id))
            return result[0]
            
        return check_reservations_result[0]
        
        