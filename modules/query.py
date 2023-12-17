from api.models import *

class Query:
    def check_duplicate_user(self, email):
        return User.objects.filter(email = email).count()
    
