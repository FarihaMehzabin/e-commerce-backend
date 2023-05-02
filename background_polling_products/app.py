from flask import Flask
import time
import mysql.connector

config = {
    "DEBUG": True,  # some Flask specific configs
}

app = Flask(__name__)

def delete_expired_reservations():
    # Replace with your own database credentials
    cnx = mysql.connector.connect(host="localhost", user="root", password="password", database="ecommerce")
    cursor = cnx.cursor()

    # Call the stored procedure to delete expired reservations
    cursor.callproc("delete_expired_reservations")
    result = None

    for row in cursor.stored_results():
        result = row.fetchone()[0]
        
    print(f"time:{time.ctime()}: result")

    if result == 0:
        cnx.commit()
    else:
        cnx.rollback()

    cursor.close()
    cnx.close()

def run_background_script():
    while True:
        print("Running background script...")
        delete_expired_reservations()
        time.sleep(60)  # Wait for 60 seconds before running again


if __name__ == "__main__":
    run_background_script()
    app.run(host='0.0.0.0', port=8081)