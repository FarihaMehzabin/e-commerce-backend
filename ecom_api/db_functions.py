import mysql.connector

class DbFunctions:
    def insert(self, statement, values):
        db_config = mysql.connector.connect(
                host="localhost", user="root", password="password", database="ecommerce",
            )
        cursor = db_config.cursor()
        
        sql = statement

        val = values

        cursor.execute(sql, val)

        db_config.commit()

        cursor.close()
        db_config.close()
        
        last_inserted_id = cursor.lastrowid

        if cursor.rowcount == 1:
            return True, last_inserted_id

        return False, 1
    
    def fetch(self, statement):
        db_config = mysql.connector.connect(
            host="localhost", user="root", password="password", database="ecommerce"
        )
        cursor = db_config.cursor()

        cursor.execute(statement)

        data = cursor.fetchall()
        
        print(data)

        cursor.close()
        db_config.close()

        return data
    
    def edit(self, statement):
        db_config = mysql.connector.connect(
            host="localhost", user="root", password="password", database="ecommerce"
        )
        cursor = db_config.cursor()

        cursor.execute(statement)
        
        print(statement)

        if cursor.rowcount > 0:
            result = "updated successfully"
        else:
            result = "No matching record found"
        
        db_config.commit()
        
        cursor.close()
        db_config.close()

        return result