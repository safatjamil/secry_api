from api.models import *


class Create:

    def secret(self, data):
        secret = Secret(user_id=data["user_id"], title=data["title"], secret=data["secret"])
        secret.save()
        return secret.id
    
    def enckey(self,data):
        enckey = EncKey(secret_id=data["secret_id"], key=data["key"])
        enckey.save()

class Update:

    def user(self, id, data):
        User.objects.filter(id = id).update(data)
    