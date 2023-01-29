import threading
import mysql.connector


class Db:
    
  def user_login(self, uname, password):
    db_config = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database='ecommerce'
  )
    cursor = db_config.cursor()
    
    print(uname, password)
    
    cursor.execute(f"SELECT CONCAT(first_name,' ', last_name), password FROM user WHERE CONCAT(first_name,' ', last_name) = '{uname}' AND password = '{password}'")

    data = cursor.fetchone()
    
    print(data)
        
    cursor.close()
    db_config.close()
        
    if data is not None:
        return True

    return False