import bcrypt
import cryptography

class Auth:

    def password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password) 

