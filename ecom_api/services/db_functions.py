import mysql.connector
from ecom_api.logger import Logger  # import your Logger class


class DbFunctions:
    def __init__(self):
        self.logger = Logger()

    class DbConnection:
        def __init__(self):
            self.db_config = None
            self.cursor = None

        def __enter__(self):
            try:
                self.db_config = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="password",
                    database="ecommerce",
                )
                self.cursor = self.db_config.cursor()
            except mysql.connector.Error as err:
                self.logger.error(f"Error connecting to the database: {err}")
                raise
            return self.cursor, self.db_config

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.cursor.close()
            self.db_config.close()

    def insert(self, statement, values):
        try:
            with self.DbConnection() as (cursor, db_config):
                cursor.execute(statement, values)
                db_config.commit()
                last_inserted_id = cursor.lastrowid

                if cursor.rowcount == 1:
                    return True, last_inserted_id
        except mysql.connector.ProgrammingError as e:
            self.logger.error(f"Programming Error executing INSERT statement: {e}")
            raise
        except mysql.connector.IntegrityError as e:
            self.logger.error(f"Integrity Error executing INSERT statement: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unknown Error executing INSERT statement: {e}")
            raise

        return False, 1

    def edit(self, statement):
        try:
            with self.DbConnection() as (cursor, db_config):
                cursor.execute(statement)

                if cursor.rowcount > 0:
                    result = "updated successfully"
                else:
                    result = "No matching record found"

                db_config.commit()
        except mysql.connector.ProgrammingError as e:
            self.logger.error(f"Programming Error executing EDIT statement: {e}")
            raise
        except mysql.connector.IntegrityError as e:
            self.logger.error(f"Integrity Error executing EDIT statement: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unknown Error executing EDIT statement: {e}")
            raise

        return result


    def fetch(self, statement):
        try:
            with self.DbConnection() as (cursor, _):
                cursor.execute(statement)
                data = cursor.fetchall()
        except Exception as e:
            self.logger.error(f"Error executing FETCH statement: {e}")
            raise

        return data

    def delete(self, statement):
        try:
            with self.DbConnection() as (cursor, db_config):
                cursor.execute(statement)

                if cursor.rowcount > 0:
                    result = "deleted successfully"
                else:
                    result = "No matching record found"

                db_config.commit()
        except Exception as e:
            self.logger.error(f"Error executing DELETE statement: {e}")
            raise

        return result

    def call_proc(self, proc, params):
        try:
            with self.DbConnection() as (cursor, db_config):
                cursor.callproc(proc, params)

                # Get the number of affected rows
                affected_rows = cursor.rowcount

                # Check if the stored procedure affected any rows
                if affected_rows > 0:
                    self.logger.info(
                        f"Stored procedure '{proc}' executed successfully, affecting {affected_rows} row(s)."
                    )

                    db_config.commit()
                    return True

                else:
                    self.logger.warning(
                        f"Stored procedure '{proc}' executed, but no rows were affected."
                    )
                    db_config.commit()
                    return False
        except Exception as e:
            self.logger.error(f"Error executing stored procedure: {e}")
            raise

    def call_proc_fetch(self, proc):
        try:
            with self.DbConnection() as (cursor, db_config):
                cursor.callproc(proc)

                # Fetch and process the results
                data = []

                for result in cursor.stored_results():
                    data.extend(result.fetchall())

                return data
        except Exception as e:
            self.logger.error(
                f"Error executing stored procedure and fetching results: {e}"
            )
            raise

    def call_proc_with_result(self, proc, params):
        try:
            with self.DbConnection() as (cursor, db_config):
                cursor.callproc(proc, params)

                # Fetch the returned result
                result = None

                # Get the first result set generated by the stored procedure
                stored_result = next(cursor.stored_results(), None)
                if stored_result:
                    result = stored_result.fetchall()

                db_config.commit()

                return result
        except Exception as e:
            self.logger.error(f"Error executing stored procedure with result: {e}")
            raise
