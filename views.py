import mysql.connector
from flask import render_template

class Views:
        
    def total_value_spent(self):
        db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
    database='ecommerce'
)

        cursor = db.cursor()
        
        cursor.execute("SELECT user.user_ID, CONCAT(user.first_name , ' ', user.last_name  )as Name, SUM(transactions.value) FROM transactions, user WHERE transactions.user_id = user.user_ID GROUP BY Name,user.user_ID ORDER BY SUM(transactions.value) DESC")
        
        result = cursor.fetchall()

        cursor.close()
        db.close()
        
        
        return render_template('total_val_spent.html', data=result)
    
    
    def top_purchased_product(self):
        db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
    database='ecommerce'
)

        cursor = db.cursor()

        cursor.execute("SELECT product.product_ID, product.name, COUNT(transactions.product_id) FROM transactions LEFT JOIN product ON transactions.product_id = product.product_ID GROUP BY product.name, product.product_ID ORDER BY COUNT(transactions.product_id) DESC LIMIT 1")
          
        result = cursor.fetchall()

        cursor.close()
        db.close()
        
        
        return render_template('top_purchased_product.html', data=result)
    
    def top_10_user(self):
        db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
    database='ecommerce'
)

        cursor = db.cursor()
                        
        cursor.execute("SELECT user.user_ID, CONCAT(user.first_name , ' ', user.last_name  )as Name, SUM(transactions.value) FROM transactions, user WHERE transactions.user_id = user.user_ID GROUP BY Name,user.user_ID ORDER BY SUM(transactions.value) DESC LIMIT 10")
        
        result = cursor.fetchall()

        cursor.close()
        db.close()
        
        
        return render_template('top_10_user.html', data=result)
        
    