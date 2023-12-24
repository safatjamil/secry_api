import bcrypt
import cryptography
import requests


class Auth:

    def password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password) 
    
    def user(self, email, password):
        url = "http://127.0.0.1:8000/api/token/"
        data = { "email": email, "password": password}
        request = requests.post(url, json = data)
        if request.status_code == 200:
            return True
        return False
                
            




