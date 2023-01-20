from time import sleep  
from json import dumps  
from kafka import KafkaProducer  
from random import randint


# initializing the Kafka producer  
my_producer = KafkaProducer(  
    bootstrap_servers = ['localhost:9092'],  
    value_serializer = lambda x:dumps(x).encode('utf-8')  
    )  

price = [100, 200, 300, 400, 500]

# generating the numbers ranging from 1 to 500  
for n in range(100):  
    productID = randint(1, 5)
    my_data = {'user_id' : randint(1, 100), 'product_id' : productID , "value": price[productID-1] }  
    my_producer.send('orders', value = my_data) 
    sleep(1)  
    
