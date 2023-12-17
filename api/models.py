from django.db import models


class User(models.Model):
    email = models.EmailField(max_length = 100)
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255, null = True, blank = True)
    password = models.BinaryField(max_length = 300)

    @classmethod
    def create(cls, dict_):
        user = cls(email = dict_["email"], first_name = dict_["first_name"], last_name = dict_["first_name"], password = dict_["password"])
        return user