from api.models import *


class Create:

    def user(self, data):
        user = User.create(data)
        user.save()
        

class Update:

    def user(self, id, data):
        User.objects.filter(id = id).update(data)
