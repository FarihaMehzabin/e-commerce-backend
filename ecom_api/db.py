import threading
import traceback
import mysql.connector
from hashing import Hashing
from db_functions import DbFunctions


class Db:
    def __init__(self):
        self.hash = Hashing()
        self.db = DbFunctions()

    def user_signup(self, fname, lname, uname, password):

        try:
            hashed_pass = self.hash.hash_pass(password)

            rowcount, id = self.db.insert(
                f"INSERT INTO user (username, first_name, last_name, password) VALUES (%s, %s, %s, %s)",
                (uname, fname, lname, hashed_pass),
            )

            return rowcount, id

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

            return False, 1

    def user_login(self, uname, password):

        res = self.db.fetch(f"SELECT * FROM user WHERE username = '{uname}'")

        data = res[0]

        if data is not None:

            hash = data[4]

            return self.hash.compare_pass(password, hash), data[0]

        return False

    def comp_signup(self, cname, uname, password):

        try:

            hashed_pass = self.hash.hash_pass(password)

            rowcount, id = self.db.insert(
                f"INSERT INTO company (name, username, password) VALUES (%s, %s, %s)",
                (cname, uname, hashed_pass),
            )

            return rowcount, id

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

            return False

    def comp_login(self, uname, password):

        res = self.db.fetch(f"SELECT * FROM company WHERE username = '{uname}'")

        data = res[0]
        
        if data is not None:

            hash = data[3]

            return self.hash.compare_pass(password, hash), data[0]

        return False

    def add_to_session_comp(self, guid, comp_id):
        try:

            self.db.insert(
                f"INSERT INTO session (guid, company_id) VALUES (%s, %s)",
                (guid, comp_id),
            )

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

            return False

    def add_to_session_user(self, guid, user_id):
        try:

            self.db.insert(
                f"INSERT INTO session (guid, user_id) VALUES (%s, %s)", (guid, user_id)
            )

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

            return False

    def check_session_comp(self, guid):

        res = self.db.fetch(
            f"SELECT guid, company_id FROM session WHERE guid = '{guid}'"
        )
        
        data = res[0]

        guid = data[0]

        comp_id = data[1]
        
        print(f"company id: {comp_id}")

        if comp_id is not None:

            res = self.db.fetch(f"SELECT name FROM company WHERE id = '{comp_id}'")
            
            data = res[0]
            
            if guid is not None:
                return True, data[0]


        return False, "no company"
    
    
    def check_session_user(self, guid):

        res = self.db.fetch(
            f"SELECT guid, user_id FROM session WHERE guid = '{guid}'"
        )
        
        data = res[0]

        guid = data[0]

        user_id = data[1]
        
        print(f"user id: {user_id}")

        if user_id is not None:

            res = self.db.fetch(
                f"SELECT first_name, last_name FROM user WHERE id = '{user_id}'"
            )
            
            data = res[0]

            if guid is not None:
                return True, data[0] + data[1]

        return False, 'No user found'
    
    def get_products(self):
        data = self.db.fetch("SELECT product.name AS product_name, product.price AS price, (SELECT Category.name FROM Category WHERE Category.id = (SELECT product_category.category_id FROM product_category WHERE product_category.product_id = product.id)) AS category_name FROM product;")
        
        print(data)
        
        return data[0], data[1], data[2]
        
        
