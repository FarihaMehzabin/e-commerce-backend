class OrderRequestResponseModel:
    def __init__(self, order_created, message, product_name = 0):
        self.order_created = order_created
        self.message = message
        self.product_name = product_name
        
    def to_dict(self):
        return {'order_created': self.order_created, 'message': self.message, 'product_name': self.product_name}
        