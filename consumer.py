# Import KafkaConsumer from Kafka library
from kafka import KafkaConsumer
from json import loads  
import mysql.connector

# Import sys module
import sys

# Define server with port
bootstrap_servers = ['localhost:9092']

# Define topic name from where the message will recieve
topicName = 'orders'

# Initialize consumer variable
consumer = KafkaConsumer (topicName, group_id ='group1',bootstrap_servers =
   bootstrap_servers, value_deserializer = lambda x : loads(x.decode('utf-8'))  )
    
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database='test'
  )

cursor = db.cursor()


for msg in consumer:
    
    print("Topic Name=%s,Message=%s"%(msg.topic,msg.value))
    sql = f"INSERT INTO transactions (user_id, product_id, value) VALUES (%s, %s, %s)"
    val = msg.value['user_id'], msg.value['product_id'], msg.value['value'] 
        
    cursor.execute(sql, val)

    db.commit()


cursor.close()
db.close()

# Terminate the script
sys.exit()