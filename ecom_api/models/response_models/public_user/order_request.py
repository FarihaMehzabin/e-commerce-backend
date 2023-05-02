class OrderRequestResponseModel:
    def __init__(self, order_created, order_id, message, product_name = "no product", total = "no total" ):
        self.order_created = order_created
        self.message = message
        self.product_name = product_name
        self.total = total
        self.order_id = order_id
        
    def to_dict(self):
        return {'order_created': self.order_created, 'message': self.message, 'product_name': self.product_name, 'total': self.total, "order_id": self.order_id}
        