import time
from ecom_api.services.db_functions import DbFunctions


class BackgroundPolling:
    
    def __init__(self):
        self.db = DbFunctions()
        
    def delete_expired_reservations(self):
       results = self.db.call_proc_fetch("delete_expired_reservations")
       
       print(results)
        
    def run_background_script(self):
        while True:
            print("Running background script...")
            self.delete_expired_reservations()
            time.sleep(60)  # Wait for 60 seconds before running again

