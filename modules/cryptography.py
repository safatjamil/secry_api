import bcrypt
import cryptography


class Encrypt:

    def hash_password(self,password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) 
    
    def encrypt_string(self, secret, key):
        fernet = Fernet(key)
        return fernet.encrypt(secret.encode('utf-8'))
 

    
