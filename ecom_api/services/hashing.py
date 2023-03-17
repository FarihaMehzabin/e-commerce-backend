import hashlib
import os
from base64 import b64encode, b64decode



class Hashing:
  
    salt = os.urandom(32)
    
    def hash_pass(self, password):
        
        digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), Hashing.salt , 10000)
        
        hex_hash = digest.hex()
        
        return hex_hash
    
    def compare_pass(self, password, hash):
        
        digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), Hashing.salt, 10000)
        
        hex_hash = digest.hex()
        
        if hash == hex_hash:
            
            print("Pass match")
            
            return True
        
        print("Pass dont match")
            
        return False
    
    def hash_guid(self, key):
        hashGen = hashlib.sha512()
        hashGen.update(key.encode())
        hash = hashGen.hexdigest()
        
        return hash
        
        
        
    