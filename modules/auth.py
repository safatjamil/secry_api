import bcrypt
import cryptography
from .query import *

query = Query()

class Auth:

    def password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password) 
    
    def user(self, email, password):
        user = query.user(email = email)
        if user is None:
            return None
    
        hashed_password = bytes(user.password[2:-1], "utf-8")
        if not self.password(password, hashed_password):
            return None 
        return user
                
            




