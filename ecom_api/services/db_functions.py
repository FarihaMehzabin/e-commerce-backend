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
