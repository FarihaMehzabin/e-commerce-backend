import datetime

class Logger:
    def __init__(self):
        self.enable_debug = False
        self.enable_info = True

    def error(self, message, source = "demo_site", user_id=None):
        self._log("ERROR", message, source, user_id)

    def warning(self, message, source = "demo_site", user_id=None):
        self._log("WARNING", message, source, user_id)

    def info(self, message, source = "demo_site", user_id=None):
        self._log("INFO", message, source, user_id, insert=self.enable_info)

    def debug(self, message, source = "demo_site", user_id=None):
        self._log("DEBUG", message, source, user_id, insert=self.enable_debug)
    
    def critical(self, message, source = "demo_site", user_id=None):
        self._log("CRITICAL", message, source, user_id)

    def _log(self, severity, message, source, user_id, insert=True):
        from ecom_api.services.db_functions import DbFunctions  
        self.db_functions = DbFunctions()

        severity_map = {
        'INFO': 0,
        'ERROR': 1,
        'WARNING': 2,
        'CRITICAL': 3,
        'DEBUG': 4,
        }
        
        timestamp = datetime.datetime.utcnow()
        
        print(f"{timestamp} | {severity} | Source: {source} | Message: {message}")

        if insert:
            insert_statement = "INSERT INTO logs (datetime, severity, message, source, user_id) VALUES (UTC_TIMESTAMP(), %s, %s, %s, %s)"
            severity_value = severity_map.get(severity, -1)
            values = (severity_value, message, source, user_id)
            success, _ = self.db_functions.insert(insert_statement, values)
