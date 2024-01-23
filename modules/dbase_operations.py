from api.models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class Create:
    def user(self, data):
        user = User.objects.create_user(email=data["email"], 
                                        password=data["password"], 
                                        first_name=data["first_name"], 
                                        last_name=data["last_name"])
        
    def secret(self, data):
        secret = Secret(user_id=data["user_id"], 
                        title=data["title"], 
                        secret=data["secret"])
        secret.save()
        return secret.id
    
    def enckey(self, data):
        enckey = EncKey(secret_id=data["secret_id"], 
                        key=data["key"])
        enckey.save()


class Update:
    def user(self, user, data):
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.save()
    
    def secret(self, secret_id, data):
        secret = Secret.objects.get(id=secret_id)
        secret.title = data["title"]
        secret.secret = data["secret"]
        secret.save()
    
    def enckey(self, secret_id, data):
        enckey = EncKey.objects.get(secret_id=secret_id)
        enckey.key = data["key"]
        enckey.save()


class Delete:
    def user(self, user):
        user.delete()
    
    def secret(self, secret_id):
        secret = Secret.objects.get(id=secret_id)
        secret.delete()
    
    def enckey(self, secret_id):
        enckey = EncKey.objects.get(secret_id=secret_id)
        enckey.delete()