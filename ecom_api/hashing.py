import hashlib
import os
from base64 import b64encode, b64decode
import secrets
import string
import mysql.connector
 

class Hashing:
  
    
    def hash_pass(self, password):
        
        salt = os.urandom(32)
        
        token = b64encode(salt).decode('utf-8')
        
        digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt , 10000)
        
        hex_hash = digest.hex()
        
        print(token)
        
        return hex_hash, token
    
    def compare_pass(self, password, salt, hash):
        
        token = b64decode(salt.encode())
        
        print(token)
        
        digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), token, 10000)
        
        hex_hash = digest.hex()
        
        if hash == hex_hash:
            return True
            
        return False
    
    def hash_guid(self, key):
        hashGen = hashlib.sha512()
        hashGen.update(key.encode())
        hash = hashGen.hexdigest()
        
        return hash
        
        
        
    