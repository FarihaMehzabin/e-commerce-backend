import threading
import mysql.connector
from hashing import Hashing


class Db:
    def __init__(self):
        self.hash = Hashing()

    def user_signup(self, fname, lname, uname, password):
        db_config = mysql.connector.connect(
            host="localhost", user="root", password="password", database="ecommerce"
        )
        cursor = db_config.cursor()

        print(uname, password)

        sql = f"INSERT INTO user (username, first_name, last_name, password, salt) VALUES (%s, %s, %s, %s, %s)"

        hashed_pass, salt = self.hash.hash_pass(password)

        val = (uname, fname, lname, hashed_pass, salt)

        cursor.execute(sql, val)

        db_config.commit()

        cursor.close()
        db_config.close()
        
        
        rows_inserted = cursor.rowcount
        
        print(rows_inserted)

        if rows_inserted == 1:
            return True

        return False

    def user_login(self, uname, password):
        db_config = mysql.connector.connect(
            host="localhost", user="root", password="password", database="ecommerce"
        )
        cursor = db_config.cursor()

        cursor.execute(f"SELECT * FROM user WHERE username = '{uname}'")

        data = cursor.fetchone()
        

        if data is not None:
            salt = data[5]
            
            hash = data[4]
            
            return self.hash.compare_pass(password, salt, hash)

        cursor.close()
        db_config.close()

        return False
