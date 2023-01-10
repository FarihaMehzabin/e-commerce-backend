from time import sleep  
from json import dumps  
from kafka import KafkaProducer  
from random import randint


# initializing the Kafka producer  
my_producer = KafkaProducer(  
    bootstrap_servers = ['localhost:9092'],  
    value_serializer = lambda x:dumps(x).encode('utf-8')  
    )  


# generating the numbers ranging from 1 to 500  
for n in range(1000):  
    my_data = {'user_id' : randint(1, 100), 'product_id' : randint(1, 100), "value": randint(100, 500) }  
    my_producer.send('orders', value = my_data) 
    sleep(1)  
    
