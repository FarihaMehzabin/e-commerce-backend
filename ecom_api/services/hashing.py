import hashlib
import os
from dotenv import load_dotenv
from ecom_api.logger import Logger

logger = Logger()

load_dotenv()

# Access the salt from the environment variables
salt_hex = os.environ["SALT"]

# Convert the salt from hex string back to bytes
salt = bytes.fromhex(salt_hex)

class Hashing:
    
    def hash_pass(self, password):
        
        digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt , 10000)
        
        hex_hash = digest.hex()
        
        return hex_hash
    
    def compare_pass(self, password, hash):
        
        digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 10000)
        
        hex_hash = digest.hex()
        
        if hash == hex_hash:
            
            logger.info("Pass match")
            
            return True
        
        logger.warning("Pass dont match")
            
        return False
    
    def hash_guid(self, key):
        hashGen = hashlib.sha512()
        hashGen.update(key.encode())
        hash = hashGen.hexdigest()
        
        return hash
        
        
        
    