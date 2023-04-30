import mysql.connector


class DbFunctions:

    class DbConnection:
        def __init__(self):
            self.db_config = None
            self.cursor = None

        def __enter__(self):
            self.db_config = mysql.connector.connect(
                host="localhost", user="root", password="password", database="ecommerce"
            )
            self.cursor = self.db_config.cursor()
            return self.cursor, self.db_config

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.cursor.close()
            self.db_config.close()

    def insert(self, statement, values):
        with self.DbConnection() as (cursor, db_config):
            cursor.execute(statement, values)
            db_config.commit()
            last_inserted_id = cursor.lastrowid

            if cursor.rowcount == 1:
                return True, last_inserted_id

        return False, 1

    def fetch(self, statement):
        with self.DbConnection() as (cursor, _):
            cursor.execute(statement)
            data = cursor.fetchall()
            print(data)

        return data

    def edit(self, statement):
        with self.DbConnection() as (cursor, db_config):
            cursor.execute(statement)
            print(statement)

            if cursor.rowcount > 0:
                result = "updated successfully"
            else:
                result = "No matching record found"

            db_config.commit()

        return result

    def delete(self, statement):
        with self.DbConnection() as (cursor, db_config):
            cursor.execute(statement)
            print(statement)

            if cursor.rowcount > 0:
                result = "deleted successfully"
            else:
                result = "No matching record found"

            db_config.commit()

        return result
    
    def call_proc(self, proc, params):
        with self.DbConnection() as (cursor, db_config):
            
            cursor.callproc(proc, params)
           
            # Get the number of affected rows
            affected_rows = cursor.rowcount

            # Check if the stored procedure affected any rows
            if affected_rows > 0:
                print(f"Stored procedure '{proc}' executed successfully, affecting {affected_rows} row(s).")
                
                db_config.commit()
                return True
            
            else:
                print(f"Stored procedure '{proc}' executed, but no rows were affected.")
                db_config.commit()
                return False

    def call_proc_fetch(self, proc):
        with self.DbConnection() as (cursor, db_config):
            
            cursor.callproc(proc)
           
            # Fetch and process the results
            data = []
            
            for result in cursor.stored_results():
                data.extend(result.fetchall())
                
            return data
        
    def call_proc_with_result(self, proc, params):
        with self.DbConnection() as (cursor, db_config):
            
            cursor.callproc(proc, params)
           
           # Fetch the returned result
            result = None
            for row in cursor.stored_results():
                result = row.fetchone()  # Get the first column of the first row
                    
            
            db_config.commit()
            
            return result
