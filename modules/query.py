from api.models import *

class Query:
    def user(self, email):
        if User.objects.filter(email = email).count() > 0:
            return User.objects.filter(email = email)[0]
        return None
    
    
