import bcrypt
import cryptography
from .query import *

query = Query()

class Auth:

    def password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password) 
    
    def user(self, email, password):
        user = query.user(email = email)
        print("a1 {}".format(email))
        if user is None:
            return None
        print("a2 {}".format(user.password))
        if not Auth.password(password, user.password):
            return None
        print("a3")
        return user
                
            




