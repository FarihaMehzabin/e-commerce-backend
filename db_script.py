import mysql.connector
import names

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database='test'
  )

cursor = db.cursor()

cursor.execute("CREATE DATABASE test")

cursor.execute(f"CREATE TABLE product (ID INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), price INT)")

cursor.execute("CREATE TABLE user (ID INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255))")

cursor.execute(f"CREATE TABLE transactions (ID INT AUTO_INCREMENT PRIMARY KEY, user_id INT, product_id INT, value INT)")

pro = ['chair', 'table', 'pen', 'pencil', 'phone']
price = 100
ind = 0

for x in range(100):
    sql = f"INSERT INTO product (name, price) VALUES (%s, %s)"
    val = pro[ind], price
    
    ind+=1
    price = price + 10
    
    if ind == 5:
        ind = 0
        
    cursor.execute(sql, val)

    db.commit()


for i in range(100):
    print(names.get_first_name())
    
    sql = f"INSERT INTO user (first_name, last_name) VALUES (%s, %s)"
    val = names.get_first_name(),names.get_last_name()
        
    cursor.execute(sql, val)

    db.commit()


cursor.close()
db.close()

