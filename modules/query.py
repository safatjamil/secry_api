from django.contrib.auth import get_user_model
from api.models import UserManager, CustomUser, Secret, EncKey

User = get_user_model()


class Query:
    def user(self, email):
        if User.objects.filter(email=email).count() > 0:
            return User.objects.filter(email=email)[0]
        return None
    
    def duplicate_user(self,email):
        return User.objects.filter(email=email).count()
    
    def secrets(self, user_id):
        return Secret.objects.filter(user_id=user_id).all()
    
    def secret(self, secret_id, user_id):
        data = {}
        data["found"] = False
        data["content"] = ""
        if Secret.objects.filter(id=secret_id, user_id=user_id).count() > 0:
            data["found"] = True
            data["content"] = Secret.objects.filter(id=secret_id, user_id=user_id).values()[0]
        return data
        
    def encr_key(self, secret_id):
        return EncKey.objects.filter(secret_id=secret_id).values()[0]
    


    
    
