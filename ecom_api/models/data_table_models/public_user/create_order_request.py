

class CreateOrderRequestDataModel:
    def __init__(self, order_data):
        self.user_id = order_data['user_id']
        self.address_line_1 = order_data['delivery']['address_line_1']
        self.city = order_data['delivery']['city']
        self.postcode = order_data['delivery']['postcode']
        self.items = order_data['items']