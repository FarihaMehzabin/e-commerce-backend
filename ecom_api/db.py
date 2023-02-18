import threading
import traceback
import mysql.connector
from hashing import Hashing


class Db:
    def __init__(self):
        self.hash = Hashing()

    def user_signup(self, fname, lname, uname, password):
        
        try:
            db_config = mysql.connector.connect(
                host="localhost", user="root", password="password", database="ecommerce"
            )
            cursor = db_config.cursor()

            print(uname, password)

            sql = f"INSERT INTO user (username, first_name, last_name, password) VALUES (%s, %s, %s, %s)"

            hashed_pass = self.hash.hash_pass(password)

            val = (uname, fname, lname, hashed_pass)

            cursor.execute(sql, val)

            db_config.commit()

            cursor.close()
            db_config.close()
            

            if cursor.rowcount == 1:
                return True

            return False
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
            
            return False

    def user_login(self, uname, password):
        db_config = mysql.connector.connect(
            host="localhost", user="root", password="password", database="ecommerce"
        )
        cursor = db_config.cursor()

        cursor.execute(f"SELECT * FROM user WHERE username = '{uname}'")

        data = cursor.fetchone()

        if data is not None:
            
            hash = data[4]
            
            return self.hash.compare_pass(password, hash)

        cursor.close()
        db_config.close()

        return False
    
    
    def comp_signup(self, cname, uname, password):
        
        try:
            db_config = mysql.connector.connect(
                host="localhost", user="root", password="password", database="ecommerce"
            )
            cursor = db_config.cursor()

            print(uname, password)

            sql = f"INSERT INTO company (name, username, password) VALUES (%s, %s, %s)"

            hashed_pass = self.hash.hash_pass(password)

            val = (cname, uname, hashed_pass)

            cursor.execute(sql, val)

            db_config.commit()
            
            last_inserted_id = cursor.lastrowid

            cursor.close()
            db_config.close()
            

            if cursor.rowcount == 1:
                return True, last_inserted_id

            return False
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
            
            return False
        
    def comp_login(self, uname, password):
        db_config = mysql.connector.connect(
            host="localhost", user="root", password="password", database="ecommerce"
        )
        cursor = db_config.cursor()

        cursor.execute(f"SELECT * FROM company WHERE username = '{uname}'")

        data = cursor.fetchone()
        
        print(data)

        if data is not None:
            
            hash = data[3]
            
            return self.hash.compare_pass(password, hash), data[0]

        cursor.close()
        db_config.close()

        return False
    
    
    def add_to_session(self, guid, comp_id):
        try:
            db_config = mysql.connector.connect(
                host="localhost", user="root", password="password", database="ecommerce"
            )
            cursor = db_config.cursor()

            sql = f"INSERT INTO session (guid, company_id) VALUES (%s, %s)"

            val = (guid, comp_id)

            cursor.execute(sql, val)

            db_config.commit()

            cursor.close()
            db_config.close()
         
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
            
            return False
        
    
    
    def check_session(self, guid):
        db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database='ecommerce'
)

        cursor = db.cursor()

        cursor.execute(f"SELECT guid, company_id FROM session WHERE guid = '{guid}'")

        data = cursor.fetchone()
        
        guid = data[0]
        
        comp_id = data[1]
        
        cursor.execute(f"SELECT name FROM company WHERE id = '{comp_id}'")

        res = cursor.fetchone()
        
        print(res)

        cursor.close()
        db.close()
        
        if guid is not None:
            return True, res[0]
        
        return False
