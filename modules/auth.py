import bcrypt
import cryptography

class Auth:

    def auth_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password) 

