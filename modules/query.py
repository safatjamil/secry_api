from django.contrib.auth import get_user_model
from api.models import *

User = get_user_model()
class Query:
    def user(self, email):
        if User.objects.filter(email = email).count() > 0:
            return User.objects.filter(email = email)[0]
        return None
    
    def duplicate_user(self,email):
        return User.objects.filter(email = email).count()
    
    
