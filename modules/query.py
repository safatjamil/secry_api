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
    
    def secrets(self, user):
        return Secret.objects.filter(user_id = user.id).all()
    
    def key(self, secret_id):
        return EncKey.objects.filter(secret_id = secret_id)
    
    
